/* Seed rule set for Bin-finder (prototype, Week 2).
 *
 * STATUS: self-curated placeholder data. Before Week 4 this must be replaced
 * line-by-line with rules transcribed from the published campus recycling guide,
 * each carrying the `source` line it came from. Nothing here may be invented.
 *
 * `hazardous: true` items are hard refusals - the app will not answer them, it
 * hands off to building staff / the hazardous-waste route.
 */

window.BIN_RULES = [
  // ---- Paper / cardboard
  { item: "newspaper",      bin: "Paper",        rule: "Clean, dry newspaper and magazines.", source: "seed-01" },
  { item: "magazine",       bin: "Paper",        rule: "Clean, dry newspaper and magazines.", source: "seed-01" },
  { item: "envelope",       bin: "Paper",        rule: "Paper envelopes, including window envelopes.", source: "seed-02" },
  { item: "cardboard box",  bin: "Paper",        rule: "Flattened corrugated cardboard.", source: "seed-03" },
  { item: "office paper",   bin: "Paper",        rule: "Clean office paper, printed or blank.", source: "seed-02" },
  { item: "pizza box",      bin: "General waste", rule: "Grease-soiled cardboard is not recyclable - food contamination.", source: "seed-04" },
  { item: "paper towel",    bin: "General waste", rule: "Used paper towel is not recyclable (soiled / short fibre).", source: "seed-05" },
  { item: "receipt",        bin: "General waste", rule: "Thermal receipt paper is not recyclable.", source: "seed-06" },

  // ---- Plastics
  { item: "water bottle",       bin: "Plastics", rule: "Rinsed PET drink bottles, lid off.", source: "seed-07" },
  { item: "plastic bottle",     bin: "Plastics", rule: "Rinsed plastic drink bottles, lid off.", source: "seed-07" },
  { item: "shampoo bottle",     bin: "Plastics", rule: "Rinsed HDPE bottles (#2).", source: "seed-08" },
  { item: "yoghurt tub",        bin: "Plastics", rule: "Rinsed rigid plastic food tubs.", source: "seed-09" },
  { item: "plastic bag",        bin: "General waste", rule: "Soft film plastic is not accepted in the plastics bin.", source: "seed-10" },
  { item: "cling film",         bin: "General waste", rule: "Soft film plastic is not accepted in the plastics bin.", source: "seed-10" },
  { item: "crisp packet",       bin: "General waste", rule: "Metallised film is not recyclable.", source: "seed-11" },
  { item: "plastic straw",      bin: "General waste", rule: "Small/light plastics fall through sorting machinery.", source: "seed-12" },
  { item: "coffee cup lid",     bin: "General waste", rule: "Mixed-material lid, not recyclable.", source: "seed-13" },

  // ---- Metals
  { item: "aluminium can",  bin: "Metals", rule: "Rinsed aluminium drink cans.", source: "seed-14" },
  { item: "tin can",        bin: "Metals", rule: "Rinsed steel food tins, label removed if loose.", source: "seed-15" },
  { item: "foil",           bin: "Metals", rule: "Clean, scrunched aluminium foil (ball at least 5cm).", source: "seed-16" },
  { item: "aerosol can",    bin: "Hazardous", rule: "Pressurised containers - do not bin, hand to staff.", source: "seed-17", hazardous: true },

  // ---- Glass
  { item: "glass bottle",  bin: "Glass", rule: "Rinsed glass bottles, lids removed.", source: "seed-18" },
  { item: "jam jar",       bin: "Glass", rule: "Rinsed glass jars, lids removed.", source: "seed-18" },
  { item: "wine glass",    bin: "General waste", rule: "Drinking glass / Pyrex has a different melting point - not container glass.", source: "seed-19" },
  { item: "mirror",        bin: "General waste", rule: "Mirrored glass is not container glass.", source: "seed-20" },

  // ---- Food / organic
  { item: "banana peel",   bin: "Food waste", rule: "Fruit and vegetable peelings.", source: "seed-21" },
  { item: "tea bag",       bin: "Food waste", rule: "Tea leaves and plain paper tea bags (remove staple if present).", source: "seed-22" },
  { item: "coffee grounds",bin: "Food waste", rule: "Coffee grounds and filter paper.", source: "seed-23" },
  { item: "egg shell",     bin: "Food waste", rule: "Eggshells and food scraps.", source: "seed-21" },
  { item: "bones",         bin: "General waste", rule: "Bones are not accepted in the food-waste stream.", source: "seed-24" },

  // ---- E-waste / special
  { item: "battery",        bin: "Hazardous", rule: "Batteries - dedicated collection point only.", source: "seed-25", hazardous: true },
  { item: "phone charger",  bin: "E-waste",    rule: "Small electronics and cables - e-waste collection point.", source: "seed-26" },
  { item: "laptop",         bin: "E-waste",    rule: "Electronics - e-waste collection point, wipe data first.", source: "seed-27" },
  { item: "light bulb",     bin: "Hazardous",  rule: "Bulbs - dedicated collection point, do not break.", source: "seed-28", hazardous: true },
  { item: "paint",          bin: "Hazardous",  rule: "Liquid paint - hazardous-waste route only.", source: "seed-29", hazardous: true },
  { item: "medicine",       bin: "Hazardous",  rule: "Medicines - pharmacy take-back, never the bin.", source: "seed-30", hazardous: true },

  // ---- Everyday non-recyclables
  { item: "cigarette butt", bin: "General waste", rule: "Cigarette butts are not recyclable.", source: "seed-31" },
  { item: "nappy",          bin: "General waste", rule: "Hygiene waste - general waste.", source: "seed-32" },
  { item: "balloon",        bin: "General waste", rule: "Foil/latex balloons - general waste.", source: "seed-33" },
  { item: "toothbrush",     bin: "General waste", rule: "Mixed-material rigid plastic - general waste.", source: "seed-34" },
  { item: "pen",            bin: "General waste", rule: "Mixed-material writing instruments - general waste.", source: "seed-35" },
];

window.BIN_FINDER_META = {
  datasetStatus: "SEED — self-curated placeholder, not yet transcribed from the published guide",
  dataSource: "seed rules (self-curated)",
  ruleCount: window.BIN_RULES.length,
};
