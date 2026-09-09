#!/usr/bin/env node
/* Bin-finder evaluation harness.
 *
 * Runs the real lookup() out of index.html against hand-written expected answers in
 * tasks.json. Expected answers are NOT derived from rules.js - that is deliberate: if
 * someone edits the rule table wrongly, this must fail rather than agree.
 *
 * Usage:  node evaluate.js
 * Exit code 0 = all gates passed, 1 = at least one gate failed.
 */

const fs = require('fs');
const path = require('path');

const here = __dirname;
const html = fs.readFileSync(path.join(here, 'index.html'), 'utf8');
const rulesSrc = fs.readFileSync(path.join(here, 'rules.js'), 'utf8');
const tasks = JSON.parse(fs.readFileSync(path.join(here, 'tasks.json'), 'utf8'));

// Load the shipped rule set and the shipped lookup logic - no reimplementation.
global.window = {};
eval(rulesSrc);
const RULES = global.window.BIN_RULES;
eval(html.match(/function norm\(s\) \{[\s\S]*?\n  \}/)[0]);
eval(html.match(/function lookup\(raw\) \{[\s\S]*?\n  \}/)[0]);

const results = { bins: [], haz: [], unknown: [], variants: [] };
let failures = 0;

function record(group, q, pass, detail) {
  results[group].push({ q, pass, detail });
  if (!pass) failures++;
}

// ---- 1. Task set: correct bin AND a citable rule -----------------------------
for (const t of tasks.bins) {
  const hit = lookup(t.q);
  if (!hit) {
    record('bins', t.q, false, 'no match at all');
    continue;
  }
  const binOk = hit.r.bin === t.expect;
  const cited = Boolean(hit.r.rule && hit.r.source);
  record('bins', t.q, binOk && cited,
    binOk ? (cited ? `ok (${hit.r.source})` : 'MISSING CITATION') : `got ${hit.r.bin}, want ${t.expect}`);
}

// ---- 2. Hazardous items must refuse, never assign a bin ----------------------
for (const t of tasks.refusals_hazardous) {
  const hit = lookup(t.q);
  const refuses = hit && hit.r.hazardous === true;
  record('haz', t.q, refuses === true,
    refuses ? 'refused (hazardous)' : `FAILED - returned ${hit ? hit.r.bin : 'no match'}`);
}

// ---- 3. Unknown items must return no match (front-end then refuses) ----------
for (const t of tasks.refusals_unknown) {
  const hit = lookup(t.q);
  record('unknown', t.q, hit === null,
    hit === null ? 'refused (not in rules)' : `FAILED - guessed ${hit.r.bin} via "${hit.r.item}"`);
}

// ---- 4. Robustness: casing / whitespace / punctuation ------------------------
for (const t of tasks.variants) {
  const hit = lookup(t.q);
  record('variants', t.q.trim(), hit !== null && hit.r.bin === t.expect,
    hit ? `got ${hit.r.bin}` : 'no match');
}

// ---- 5. Every rule is cited --------------------------------------------------
let uncited = RULES.filter(r => !r.rule || !r.source);

// ---- Report ------------------------------------------------------------------
function pct(list) {
  const p = list.filter(x => x.pass).length;
  return `${p}/${list.length} (${Math.round((p / list.length) * 100)}%)`;
}

const lines = [];
const say = s => { lines.push(s); console.log(s); };

say('Bin-finder evaluation');
say('=' .repeat(60));
say(`rule set: ${RULES.length} rules | hazardous: ${RULES.filter(r => r.hazardous).length}`);
say('data: SEED (self-curated placeholder)');
say('');
say(`1. Task set (correct bin + citation)   ${pct(results.bins)}`);
results.bins.filter(r => !r.pass).forEach(r => say(`     FAIL  ${r.q}: ${r.detail}`));
say(`2. Hazardous refusals                  ${pct(results.haz)}`);
results.haz.filter(r => !r.pass).forEach(r => say(`     FAIL  ${r.q}: ${r.detail}`));
say(`3. Unknown-item refusals               ${pct(results.unknown)}`);
results.unknown.filter(r => !r.pass).forEach(r => say(`     FAIL  ${r.q}: ${r.detail}`));
say(`4. Input robustness                    ${pct(results.variants)}`);
results.variants.filter(r => !r.pass).forEach(r => say(`     FAIL  ${r.q}: ${r.detail}`));
say(`5. Every rule carries a source line    ${RULES.length - uncited.length}/${RULES.length}`);
uncited.forEach(r => say(`     FAIL  "${r.item}" has no rule/source`));
say('');

const hazOk = results.haz.every(r => r.pass);
const unkOk = results.unknown.every(r => r.pass);
const binPct = results.bins.filter(r => r.pass).length / results.bins.length;
const gates = [
  ['task set >= 90%', binPct >= 0.9, `${Math.round(binPct * 100)}%`],
  ['hazardous refusals 100%', hazOk, hazOk ? 'pass' : 'FAIL'],
  ['unknown refusals 100%', unkOk, unkOk ? 'pass' : 'FAIL'],
  ['every rule cited', uncited.length === 0, uncited.length === 0 ? 'pass' : 'FAIL'],
];
say('Gates ("good enough")');
gates.forEach(([name, ok, val]) => say(`  ${ok ? 'PASS' : 'FAIL'}  ${name.padEnd(26)} ${val}`));
say('');
say(failures === 0 && uncited.length === 0 ? 'RESULT: ALL GATES PASSED' : `RESULT: ${failures} failure(s)`);

fs.writeFileSync(path.join(here, 'eval-results.txt'), lines.join('\n') + '\n');
process.exit(failures === 0 && uncited.length === 0 ? 0 : 1);
