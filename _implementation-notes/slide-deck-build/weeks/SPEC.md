# Slide-content extraction spec (FotH GS club deck, weeks 3-22)

For EACH assigned week, read its lesson plan (path in roads.json) and produce `week<NN>.json`
(two digits, e.g. week03.json) in THIS directory (the directory this SPEC.md is in).

## What to generate
One JSON slide entry per road stop (roads.json lists each week's stops in order), EXCEPT skip
stops whose text is essentially: "Welcome and centering", "Welcome and opening container",
"Opening container" (any variant), "Closing container" (+ blessing), "Leader Feedback Round".
Those are standing slides inserted automatically. DO generate slides for welcome stops that
carry real teaching (e.g. Week 21 "Welcome and integration teaching", Week 22 "Welcome and framing").

## JSON schema
{"week": 3, "slides": [
  {"stop": 2,                       // 1-based index into that week's stops array
   "title": "Check-In on Week 2 Practice",   // short, Title Case, may echo the stop text
   "items": [
     {"kind":"bullet","text":"..."},              // top-level point
     {"kind":"sub","text":"...","italic":true},   // indented detail/quote; italic optional
     {"kind":"numbered","num":1,"text":"..."}     // numbered step/question
   ],
   "panel": {"label":"PSALM 139:23–24","lines":["“Search me, O God, and know my heart…”"]}  // OPTIONAL
  }]}

## Style rules (the deck carries the room; the plan carries the script)
- 3–6 items per slide. Short lines a participant can read aloud from across a circle.
- Quote the plan's spoken lines verbatim inside curly quotes where the room hears/says them.
- Scripture: if the plan quotes the verse text, put the full quote in "panel" with the reference
  as the label (caps). If the plan gives only a reference, mention the reference in an item —
  NEVER compose verse text yourself.
- Questions the room will answer: use the plan's exact wording.
- Em dashes are house style. Keep the plan's vocabulary (container, cluster, Companion, rhema…).
- Practice slides: state the week's practice concretely (what, how often, how long).
- Do not invent content absent from the plan; compress, don't paraphrase into new claims.
- At most ONE panel per slide. Panels are for scripture or short liturgical text read aloud.

## Example (from the already-built Week 2, for calibration)
{"stop": 4, "title": "Family Clusters — the Heart Soil Diagnostic",
 "items": [
  {"kind":"bullet","text":"Not “which soil am I?” — where does each soil show up in my life right now? Specifically."},
  {"kind":"numbered","num":1,"text":"Path — where is the ground hard right now? One specific place, this week"},
  {"kind":"numbered","num":2,"text":"Rocky — where has a season with God not lasted? What sun revealed the missing roots?"},
  {"kind":"numbered","num":3,"text":"Thorny — what is choking me right now: cares, riches, other desires? Which is loudest?"},
  {"kind":"numbered","num":4,"text":"Good — where has something God planted actually grown? Name one real piece of fruit"},
  {"kind":"bullet","text":"Journal two minutes, then share — a parent answers first, every round"},
  {"kind":"bullet","text":"“I’d rather not share that one” is a complete answer — a gift, not ammunition"}]}

Return (as your final message) ONLY a one-line summary per week: week number, slide count, any stop you could not map.
