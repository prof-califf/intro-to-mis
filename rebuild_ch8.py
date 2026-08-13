# SUPERSEDED: chapter8-ai-ml.html is now the canonical source; do not re-run.
"""Rebuilds chapter8-ai-ml.html with the TikTok-first arc: the familiar win opens,
the Amazon hiring tool becomes the turn. Sections 7+ (Wrapped, jobs, other side,
components, summary, TPS, DQs, sources) are preserved from the current file with
targeted edits. This file supersedes the CH8 block in build_ch7_ch8.py.
"""
import re

t = open('chapter8-ai-ml.html').read()
HEAD = t[:t.index('<main class="chapwrap">')]
BACK = t[t.index('<h2 id="s7"'):]          # Wrapped onward, kept
# retitle
HEAD = HEAD.replace('<title>Chapter 8: AI, Machine Learning &amp; Bias | MIS 320</title>',
                    '<title>Chapter 8: AI &amp; Machine Learning: TikTok to the Hiring Desk | MIS 320</title>')
HEAD = re.sub(r'<meta name="description" content="[^"]*">',
 '<meta name="description" content="From the For You page that knows you in an evening to the hiring model Amazon had to kill: what machine learning is, why one idea produces both, and who decides which you get.">',
 HEAD, count=1)

FRONT = '''<main class="chapwrap">

<header class="chaphead">
  <p class="eyebrow">Chapter 8 &middot; AI, Machine Learning &amp; Bias</p>
  <h1>AI and Machine Learning: From the For You Page to the Hiring Desk</h1>
  <p class="anchor">Open TikTok on a brand-new account and the feed is generic. Within an evening it
  knows you: your humor, your sport, the niche you did not know had a name. That uncanny accuracy is
  machine learning, the most consequential business technology of your working lifetime, and the same
  idea flags fraud before your card clears, folds proteins that won a Nobel Prize, and wrote 1.4
  billion Wrapped stories last year. It is also the idea that, pointed at a decade of resumes, taught
  an Amazon hiring engine to prefer men. One kind of math, both outcomes. This chapter is about how
  that is possible, and why the people running these systems, not the systems, decide which one you
  get.</p>
  <div class="meta-row">
    <span>Cases: TikTok &middot; Amazon (2014&ndash;18) &middot; Spotify Wrapped Archive (2025)</span>
    <span class="alt">Week 10 &middot; Monday</span>
    <span class="alt"><a href="schedule.html" style="color:inherit;text-decoration:none">Wednesday: what computing costs &#8594;</a></span>
  </div>
</header>

<div class="statrow">
  <div class="stat"><b>1B+</b><span>users teaching TikTok's model, every swipe</span></div>
  <div class="stat"><b>10 yrs</b><span>of resumes as Amazon's training data</span></div>
  <div class="stat"><b>1&ndash;5</b><span>stars per applicant, like a product</span></div>
  <div class="stat"><b>1.4B</b><span>LLM-written Wrapped reports</span></div>
  <div class="stat"><b>1</b><span>idea behind all of it: learn from examples</span></div>
</div>

<div class="toc"><strong>Contents</strong>
<a href="#s1">1. The machine that knows you by bedtime</a>
<a href="#s2">2. What AI actually is</a>
<a href="#s3">3. How a model learns, and what learning buys</a>
<a href="#s4">4. The turn: the model that scored people</a>
<a href="#s5">5. Bias in, bias out</a>
<a href="#s6">6. The feedback loop</a>
<a href="#s7">7. Generative AI at 1.4 billion</a>
<a href="#s8">8. What business people do with AI</a>
<a href="#s9">9. The other side: the people in the data</a>
<a href="#s10">10. The five components</a>
<a href="#s11">11. Summary and vocabulary</a>
<a href="#questions">12. Discussion questions</a>
</div>

<div class="plan">
<div class="plan-head">Monday session plan &middot; 80 minutes &middot; Week 10 (Wednesday is cloud and what computing costs)</div>
<table>
<tr><td class="t">0:00</td><td class="w">Open</td><td>Ask the room: how long did it take TikTok's For You page to figure you out, and what did it figure out that you never typed anywhere? Collect a few answers. Everyone has one, and every answer is a machine-learning system report from a user's chair.</td></tr>
<tr><td class="t">0:05</td><td class="w">Lecture</td><td>What ML is: patterns learned from data, not rules written by hand. Walk the For You page as the anatomy of supervised learning, then widen the ledger: fraud flags, folded proteins, a third of Amazon's sales. Students should be genuinely impressed before the turn.</td></tr>
<tr><td class="t">0:30</td><td class="w">Lecture</td><td>The turn: the identical math, pointed at ten years of resumes, and the "women's" penalty nobody wrote. Bias in, bias out, why editing terms could not fix it, then the feedback loop: the For You rabbit hole as the gentle version, predictive policing as the consequential one.</td></tr>
<tr><td class="t">0:50</td><td class="w">Think-pair-share</td><td>The tool works; now what? See the activity below.</td></tr>
<tr><td class="t">1:10</td><td class="w">Close</td><td>Wrapped Archive in five minutes: 1.4 billion grounded LLM reports, and Spotify's own engineers saying the model call was the easy part. It bridges directly to Wednesday: all of this runs on hardware somebody pays for.</td></tr>
</table></div>

<h2 id="s1"><span class="num">01</span>The machine that knows you by bedtime</h2>

<p>TikTok's For You page is the most personally familiar machine-learning system on earth, which
makes it the right place to start. There is no channel to subscribe to and no search you must run;
the feed simply decides, video by video, what you see next. Its raw material is your behavior: what
you watched to the end, what you rewatched, what you skipped in under a second, what you liked,
shared, or lingered on at two in the morning. TikTok's own description of the system lists exactly
these signals, weighted by how strongly each predicts your interest, with a full watch counting for
far more than a casual like. Every swipe is a training example, which is why a feed that starts
generic is uncannily yours within an evening.</p>

<p>Treat it as a business case for a moment, because it is a spectacular one. Short video was not a
new idea; the recommender was the product. Incumbents with vastly more money and data cloned the
format, and TikTok still grew past a billion monthly users, because the differentiator was not the
video player anyone could copy but the learned model no one could. When Washington later moved to
force a sale of TikTok's US operations, the hardest question in the negotiation was who would control
the algorithm, which tells you what everyone involved understood the company to actually be. A
learned model as the core asset of a hundred-billion-dollar business: that is what this chapter's
technology can do, and your generation's companies will be full of attempts to repeat it.</p>

<p>Hold one Chapter 7 thought as we go: the model does not optimize for your wellbeing or even your
taste. It optimizes for <strong>engagement</strong>, watch time and return visits, because those are
measurable proxies for satisfaction. You know from the Moneyball chapter what eventually happens when
a proxy becomes the target. Pin that; Section 6 comes back for it.</p>

<h2 id="s2"><span class="num">02</span>What AI actually is</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">AI, machine learning, and generative AI</span>
<p><strong>Artificial intelligence</strong> is the broad project of making computers do things that
seem to require intelligence. For decades the main approach was writing explicit rules. <strong>Machine
learning (ML)</strong>, the approach behind nearly everything now called AI, inverts that: instead of
writing rules, you show the system many examples and it finds the patterns itself. <strong>Generative
AI</strong>, including the <strong>large language models (LLMs)</strong> you have used all quarter
under the Lab 1 rules, is machine learning trained on so much text that the learned patterns can
produce new text, not just score or sort existing things. One family, three generations, and one
constant: the system's behavior comes from its training data, not from anyone's stated intentions.</p></div>

<p>The distinction between rules and learning matters for business because it relocates
responsibility. A rule-based system does what someone wrote, and a bad outcome traces to a bad rule
someone can find and fix. Nobody at TikTok wrote a rule that says "show this person otter videos";
the preference was learned from behavior, and it lives in millions of model parameters no manager can
read. That opacity is harmless when the stakes are otters. The rest of this chapter is about what
happens as the stakes rise, which is why it is mostly about data, not algorithms.</p>

<h2 id="s3"><span class="num">03</span>How a model learns, and what learning buys</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Training data, labels, and supervised learning</span>
<p>The workhorse of business ML is <strong>supervised learning</strong>: assemble
<strong>training data</strong>, historical examples, each carrying a <strong>label</strong>, the
outcome you want predicted, and the model adjusts itself until its predictions match the labels. Then
comes <strong>inference</strong>: applying the trained model to new cases. The For You page is a
clean specimen. Examples: videos, described by their content and by who engaged with them. Label: did
this user keep watching? Inference: run that prediction over candidate videos every time you swipe,
and serve the winner. Its sibling, <strong>unsupervised learning</strong>, finds structure with no
labels at all, like clustering the co-op's members into segments nobody predefined.</p></div>

<p>The lineage of the For You page runs straight through this course's other retail giant. Amazon's
"customers who bought this also bought" machinery works the same way, learning from millions of past
purchases via <strong>collaborative filtering</strong>; its engineers published the core item-to-item
method back in 2003, and a widely cited McKinsey estimate has put roughly 35 percent of Amazon's
sales behind its recommendations. The same learned-pattern machinery drives the demand forecasts that
place inventory in warehouses before you order.</p>

<p>And retail is one entry in a long ledger. The same machinery flags credit-card fraud in the
milliseconds between swipe and approval, which is why your bank texts you about a suspicious charge
before you have left the store. In medicine, models trained on labeled scans have matched specialist
performance at detecting diabetic retinopathy and certain cancers in published studies, extending
screening to clinics that have no specialist. DeepMind's AlphaFold predicted the three-dimensional
structure of essentially every known protein, work that earned a share of the 2024 Nobel Prize in
Chemistry and compressed months of laboratory effort per protein into minutes. Machine translation
and speech recognition have quietly become accessibility infrastructure for hundreds of millions of
people. None of this is hype; it is deployed, audited, and paying for itself, and it is why every
serious company is asking where learned prediction fits its own operations, a question someone with
your degree will be in the room for.</p>

<p>Before the turn, compress the mechanism into one sentence and keep it: <em>a supervised model is
a machine for making the future resemble the labeled past.</em> When the past is what you want more
of, that is a superpower. The next two sections are about when it is not.</p>

<h2 id="s4"><span class="num">04</span>The turn: the model that scored people</h2>

<p>Now the same idea, aimed one domain too far. Beginning in 2014, a team at Amazon built
experimental models to do for recruiting what the company had done for retail: read each incoming
resume and score the applicant from one to five stars, the way shoppers score products. One insider
described the dream to Reuters: give the engine one hundred resumes, it spits out the top five, you
hire those. This was not a rogue project by people who misunderstood the company; it was the
company's most proven idea, prediction from history, applied to its own front door.</p>

<p>To learn what a strong applicant looked like, the models trained on ten years of the company's
past resumes and how those candidacies had turned out. Here is the whole story in one sentence:
<strong>the tech industry's past applicants were mostly men, so the model learned that resumes
resembling men's resumes were what success looked like.</strong> By 2015 the team found the system
penalizing resumes containing the word "women's", as in "women's chess club captain", and downgrading
graduates of two all-women's colleges, while favoring verbs that happened to be more common on male
engineers' resumes, like "executed" and "captured".</p>

<p>Amazon edited the model to neutralize those terms, then confronted the harder truth: with tens of
thousands of terms in play, there was no way to be confident it had not found other, subtler proxies
for gender. The company lost confidence and shut the project down, telling Reuters the tool was never
used by recruiters to evaluate candidates. Note the shape of the failure before the next section
names it: nobody wrote a biased rule. Nobody wrote any rule. The system did exactly what Section 3
said supervised learning does, faithfully. The labels were the problem, because the labels were
history, and history had a skew.</p>

<div class="pull"><p>The model that found your niche by bedtime and the model that rejected her resume are the same idea. Only the training data, and the stakes, differ.</p></div>

<h2 id="s5"><span class="num">05</span>Bias in, bias out</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Training-data bias and proxy discrimination</span>
<p><strong>Training-data bias</strong> is a skew in the examples that the model faithfully learns and
reproduces; the model is not malfunctioning, which is what makes it dangerous. <strong>Proxy
discrimination</strong> is the sequel: remove the forbidden attribute, here gender, and the model
finds stand-ins that correlate with it, a word, a college, a verb, a zip code. Amazon could delete
the "women's" penalty, but could never certify the absence of every subtler proxy in fifty thousand
terms, and that impossibility, not the one embarrassing term, is why the project died.</p></div>

<p>Two management lessons hide in the ending. First, "the algorithm decided" is never an explanation:
a model's decisions are its training data's decisions, laundered through math, and accountability for
them belongs to the people who chose the data and shipped the system, a direct echo of Chapter 10's
responsibility-versus-accountability distinction. Second, Amazon's least celebrated act here was its
best one: it tested its own system, found the failure, and killed a project it had wanted badly. The
discussion questions will ask whether you would have had the nerve.</p>

<h2 id="s6"><span class="num">06</span>The feedback loop</h2>

<p>Now collect the pin from Section 1. The For You page does not just learn from your behavior; it
shapes the behavior it will learn from next. Serve what held your attention, attention becomes the
data, the data narrows what gets served. In 2021 the Wall Street Journal ran automated accounts
through TikTok and showed that watch time alone steered fresh feeds into narrow tunnels within hours,
including, for accounts that lingered on sad content, feeds that drifted toward ever darker variants
of whatever held attention. Engagement is a proxy for satisfaction, the proxy became the target, and
Chapter 7 told you the rest. For an individual user this is rabbit holes and lost evenings, worth
taking seriously and mostly recoverable.</p>

<p>Raise the stakes and the same structure stops being recoverable. <strong>Predictive
policing</strong> systems forecast where crime is likeliest and route patrols there. More patrols in
a neighborhood observe more offenses there, which enters the data as more recorded crime, which
raises the forecast, which sends more patrols. The model's prediction manufactures its own
confirmation, and historical over-policing hardens into mathematically laundered permanent policy,
applied to people who cannot log off.</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Feedback loops</span>
<p>A <strong>feedback loop</strong> exists when a system's outputs alter the inputs it will learn
from next. Recommendation engines have gentle ones; predictive systems that direct real-world action,
patrols, loans, audits, hiring, have consequential ones, because the model changes the world that
generates its evidence. The test to carry into any AI deployment: <em>does acting on this prediction
change the data that will judge the prediction?</em> If yes, the model can be confidently,
self-certifyingly wrong, and the gap between a rabbit hole and a patrol pattern is only the stakes.</p></div>

'''

out = HEAD + FRONT + BACK
open('chapter8-ai-ml.html','w').write(out)
print('rebuilt:', len(out))

# ---- targeted edits to the preserved back half ----
t = open('chapter8-ai-ml.html').read()
E = []
# other-side: one line acknowledging the attention economy alongside existing content
E.append(('Every system in this chapter runs on data generated by people who never signed up to be training\nexamples.',
          'Every system in this chapter runs on data generated by people who never signed up to be training\nexamples, and one of them, the feed, pays for itself with the attention it harvests.'))
# components table: data row now spans all three cases
E.append(('<td>Ten years of resumes; a year of listening; arrest records</td>',
          '<td>Every swipe; ten years of resumes; a year of listening; arrest records</td>'))
# summary table first rows reflect the new arc
E.append(("<tr><td><strong>The upside is real</strong></td><td>Fraud flags, folded proteins, screening where no specialist works</td>",
          "<tr><td><strong>The upside is real</strong></td><td>The feed that knows you, fraud flags, folded proteins</td>"))
# DQ4: TikTok is now in-chapter, so ask for a loop beyond both cases
E.append(('Find a feedback loop in a domain other than policing, somewhere a prediction changes the data',
          'Find a feedback loop in a domain other than policing or your own feed, somewhere a prediction changes the data'))
# add a TikTok/Goodhart DQ as question 2
E.append(('<li>Design the audit that would have caught the resume tool before launch',
          '<li>Watch time is engagement\'s batting average: measurable, and not the thing anyone actually cares about. Propose the OBP: a feed metric that better tracks whether users are glad they opened the app, and say why no platform reports it.<span class="tag tag-warm">Connect</span></li>\n<li>Design the audit that would have caught the resume tool before launch'))
# sources: add TikTok references before the McKinsey note
E.append(('<li>The McKinsey figure',
          '<li>TikTok Newsroom, <em>How TikTok recommends videos #ForYou</em> (2020): the company\'s own description of the For You system and its ranked engagement signals.</li>\n<li>Wall Street Journal, <em>Inside TikTok\'s Algorithm</em> video investigation (2021): the bot experiment showing watch time alone steering fresh accounts into narrow content tunnels within hours.</li>\n<li>The McKinsey figure'))
n=0
for old,new in E:
    if old in t: t=t.replace(old,new); n+=1
    else: print('MISS:', old[:60])
open('chapter8-ai-ml.html','w').write(t)
print('back-half edits:', n, 'of', len(E))
