"""Builds chapter7-moneyball.html and chapter8-ai-ml.html from the ch9 shell,
then updates nav menus site-wide, the schedule links, and the index cards."""
import re, glob

ch9 = open('chapter9-changehealthcare.html').read()
HEAD = ch9[:ch9.index('<main class="chapwrap">')]
TAIL = ch9[ch9.index('</main>'):]

def make_head(title, desc, eyebrow_current):
    h = HEAD
    h = re.sub(r'<title>[^<]*</title>', '<title>%s | MIS 320</title>' % title, h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="%s">' % desc, h, count=1)
    # clear ch9's current marker; the site-wide pass will set the right one
    h = h.replace('class="current" href="chapter9-changehealthcare.html"', 'href="chapter9-changehealthcare.html"')
    return h

# ============================================================ CHAPTER 7
CH7 = make_head("Chapter 7: Business Intelligence: Moneyball",
 "The 2002 Oakland A's: how measuring the right thing beat three times the payroll, and what that has to do with dashboards, KPIs, and the co-op's hidden problem.", 'ch7')

CH7 += '''<main class="chapwrap">

<header class="chaphead">
  <p class="eyebrow">Chapter 7 &middot; Business Intelligence &amp; Analytics</p>
  <h1>Business Intelligence: The Team That Measured Differently</h1>
  <p class="anchor">In 2002 the Oakland Athletics lost their three best players, fielded one of the
  cheapest rosters in baseball, and won 103 games, including twenty in a row, an American League record.
  They did it by noticing that an entire industry had spent a century measuring the wrong thing. This
  chapter is about what business intelligence actually is, why choosing the metric is the decision that
  matters, and why you have already done this analysis yourself, on Cascadia, in Lab 5.</p>
  <div class="meta-row">
    <span>Case: Oakland Athletics, 2002</span>
    <span class="alt">Week 6 &middot; Monday concepts, Wednesday case</span>
    <span class="alt"><a href="lab6-tableau.html" style="color:inherit;text-decoration:none">Paired lab: Tableau (Lab 6) &#8594;</a></span>
  </div>
</header>

<div class="statrow">
  <div class="stat"><b>~$41M</b><span>A's payroll, third lowest in MLB</span></div>
  <div class="stat"><b>~$125M</b><span>Yankees payroll, the team they had to beat</span></div>
  <div class="stat"><b>103&ndash;59</b><span>Oakland's record</span></div>
  <div class="stat"><b>20</b><span>straight wins, an AL record</span></div>
  <div class="stat"><b>1</b><span>question: what actually causes runs?</span></div>
</div>

<div class="toc"><strong>Contents</strong>
<a href="#s1">1. Losing three stars</a>
<a href="#s2">2. What business intelligence actually is</a>
<a href="#s3">3. The wrong number on the scoreboard</a>
<a href="#s4">4. Buying what the market mispriced</a>
<a href="#s5">5. Correlation, causation, and small samples</a>
<a href="#s6">6. When the metric becomes the target</a>
<a href="#s7">7. From the dugout to the dashboard</a>
<a href="#s8">8. The other side: being measured</a>
<a href="#s9">9. The five components</a>
<a href="#s10">10. Summary and vocabulary</a>
<a href="#questions">11. Discussion questions</a>
</div>

<div class="plan">
<div class="plan-head">Monday session plan &middot; 80 minutes &middot; concepts (the case is Wednesday)</div>
<table>
<tr><td class="t">0:00</td><td class="w">Open</td><td>Put two payroll numbers on the board, $41 million and $125 million, and ask what a fair season between those two teams looks like. Then reveal that the cheap one won more games. Do not explain yet.</td></tr>
<tr><td class="t">0:05</td><td class="w">Lecture</td><td>What BI is and is not: the four kinds of analytics walked on one example (last month's sales), then the batting average versus on-base percentage story as the anatomy of a proxy metric.</td></tr>
<tr><td class="t">0:35</td><td class="w">Lecture</td><td>The BI stack: operational systems, the warehouse, the dashboard. Connect straight to Lab 5: their pivot tables were descriptive and diagnostic analytics, whether or not anyone said the words.</td></tr>
<tr><td class="t">0:55</td><td class="w">Think-pair-share</td><td>A metric that made a business worse. See the activity below.</td></tr>
<tr><td class="t">1:15</td><td class="w">Close</td><td>Assign the chapter and the discussion questions for Wednesday's group presentations. Preview: this week's lab builds the dashboard the A's front office would have wanted.</td></tr>
</table></div>

<h2 id="s1"><span class="num">01</span>Losing three stars</h2>

<p>After the 2001 season, the Oakland Athletics lost their best hitter, Jason Giambi, to the New York
Yankees on a seven-year, $120 million contract, and lost outfielder Johnny Damon and closer Jason
Isringhausen the same winter. Oakland could not outbid anyone: its payroll of roughly $41 million was
the third lowest in Major League Baseball, against the Yankees' roughly $125 million. By every
conventional measure, the 2002 A's were supposed to collapse.</p>

<p>General manager Billy Beane and his assistant Paul DePodesta could not buy the players everyone
agreed were good, so they asked a more basic question: is everyone right about who is good? Baseball
had a century of meticulous statistics and a settled consensus about which ones mattered. Beane and
DePodesta treated that consensus as a hypothesis rather than a fact, tested it against the data, and
found it wrong in an exploitable way. Then they built a roster out of the players the market had
mispriced: a catcher with a damaged arm converted to first base, a sidearm reliever nobody wanted, and
hitters who looked wrong and walked constantly.</p>

<p>The result was 103 wins, a division title, and a twenty-game winning streak that set an American
League record, capped by a walk-off home run from Scott Hatteberg, the converted catcher. The season
became Michael Lewis's book <em>Moneyball</em> and later the film. But strip away the baseball and what
remains is the cleanest business intelligence case ever documented: an organization that gained a
competitive advantage not by having more data than its rivals, because everyone had the same data, but
by <strong>measuring the right thing</strong> while everyone else measured the wrong one.</p>

<h2 id="s2"><span class="num">02</span>What business intelligence actually is</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Business intelligence &amp; analytics</span>
<p><strong>Business intelligence (BI)</strong> is the practice of turning an organization's data into
information that supports decisions: the systems, reports, and dashboards that tell a business what is
happening. <strong>Analytics</strong> is the analytical work layered on top, and it comes in four
kinds, in rising order of ambition. <strong>Descriptive</strong>: what happened? <strong>Diagnostic</strong>:
why did it happen? <strong>Predictive</strong>: what will happen? <strong>Prescriptive</strong>: what
should we do about it? A monthly sales report is descriptive. Drilling into why Bellingham's number
moved is diagnostic. A forecast is predictive. A recommended reorder quantity is prescriptive.</p></div>

<p>You have been doing this for four weeks without the vocabulary. Lab 2's totals were descriptive
analytics. Lab 5's mini project, where something was wrong at Cascadia and you had to find out what,
was diagnostic analytics, and the forecasting section was your first predictive step. The ladder
matters because each rung is worth more and costs more: most organizations live on the bottom rung,
drowning in descriptive reports, and the ones that climb are the ones that turn data into different
decisions rather than prettier summaries.</p>

<p>Baseball in 2001 was a perfect specimen of a descriptive-analytics industry. It had more data per
event than almost any business on earth, a box score for every game since the 1870s, and it used that
mountain of data mostly to describe, not to question. The questioning, when it came, came from outside:
a night-shift statistician named Bill James had spent two decades publishing analyses, under the name
<strong>sabermetrics</strong>, showing that some of baseball's most cherished numbers barely predicted
winning. The A's were simply the first team desperate enough to act on it.</p>

<h2 id="s3"><span class="num">03</span>The wrong number on the scoreboard</h2>

<p>For a century, the headline measure of a hitter was <strong>batting average</strong>: hits divided
by at-bats. It is intuitive, traditional, and printed on the back of every card. It also has a design
flaw: it ignores walks entirely. A player who draws a walk has reached base, avoided an out, and
advanced the inning, and batting average records that event as if it never happened.</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Metrics, proxies, and measurement validity</span>
<p>A <strong>metric</strong> is a number chosen to stand in for something you actually care about, and
that makes almost every metric a <strong>proxy</strong>. The thing baseball cares about is winning;
wins come from runs; runs come from not making outs. <strong>Measurement validity</strong> asks: does
the proxy actually track the thing? Batting average tracks run-scoring loosely. <strong>On-base
percentage (OBP)</strong>, which counts every way of reaching base including walks, tracks it far more
tightly, because it is really measuring the avoidance of outs, and outs are the game's true scarce
resource: you only get twenty-seven. The A's insight, distilled: the industry's headline metric had
weak validity, a better one was sitting in the same box score, and nobody's prices reflected it.</p></div>

<p>Notice what kind of insight this is. It required no new technology, no new data, and no advanced
math; OBP had been recorded for decades. It required someone to ask whether the number everyone stared
at actually measured what they assumed it measured. That question, not the software, is the core skill
of business intelligence, and it transfers directly: a store's revenue is a batting average. It tells
you something happened. It does not tell you whether the underlying engine of the business, at Cascadia
the membership relationship, is healthy or quietly failing.</p>

<div class="pull"><p>The scoreboard was fine. The industry was reading the wrong line of it.</p></div>

<h2 id="s4"><span class="num">04</span>Buying what the market mispriced</h2>

<p>A mismeasured quality becomes a mispriced asset. Because the market paid for batting average, home
runs, and how an athlete looked in uniform, players who merely got on base relentlessly came cheap.
Hatteberg, coming off a career-threatening injury and hitting for modest averages, was exactly that:
his on-base skills made him a bargain, and in 2002 he posted a .374 OBP and hit the home run that won
game twenty of the streak. Reliever Chad Bradford threw underhand, looked unorthodox, got outs, and
cost almost nothing. The roster was an arbitrage portfolio.</p>

<p>Connect this to Chapter 2. Porter would say the A's found a <strong>competitive advantage grounded
in information</strong>: everyone had the same raw data, but Oakland converted it into a truer model of
value than its rivals used, which let a $41 million payroll buy roughly as much real production as
teams spending three times more. And, exactly as Chapter 2 predicts, the advantage decayed as the
information spread. Boston hired sabermetric thinkers and won the 2004 World Series; within a decade
every front office employed analysts; and once everyone measured correctly, the edge returned to the
teams with the most money. An information advantage is real, and it is rented, not owned.</p>

<h2 id="s5"><span class="num">05</span>Correlation, causation, and small samples</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Correlation, causation, and sample size</span>
<p>Two numbers are <strong>correlated</strong> when they move together; <strong>causation</strong>
means one actually drives the other. Team OBP correlates strongly with runs scored across a 162-game
season, and there is a causal mechanism behind the correlation: not making outs extends innings. That
combination, correlation plus a mechanism, tested across a large sample, is what earned the A's their
confidence. But the same logic warns you where the model stops working: a five-game playoff series is
a <strong>small sample</strong>, small enough for luck to swamp skill, which is why the 103-win A's
could lose their playoff series and why Beane himself said his approach could not be counted on in
October. The lesson is symmetric: enough data makes patterns trustworthy, and small samples make even
true patterns unreliable.</p></div>

<p>Business runs on small samples more than it admits. One viral month, one bad quarter, one focus
group of nine people. The Cascadia connection is direct: your Lab 5 forecast extrapolated from months
of data, and the honest analyst's question, there and everywhere, is whether the sample behind a
pattern is large enough to bet on. A twenty-game winning streak is thrilling and it is also, as the
A's themselves would tell you, partly a run of luck sitting on top of a genuinely good team.</p>

<h2 id="s6"><span class="num">06</span>When the metric becomes the target</h2>

<p>There is a trap waiting inside every successful metric, and it has a name: <strong>Goodhart's
law</strong>, usually stated as <em>when a measure becomes a target, it ceases to be a good
measure</em>. The moment you pay people on a number, they optimize the number, not the thing it was a
proxy for, and the gap between the two becomes the business's blind spot.</p>

<p>Call centers that grade agents on average handle time get shorter calls and angrier customers,
because the fastest way to end a call is to not solve the problem. Schools graded on test scores drift
toward teaching the test. A sales team paid on units shipped will stuff the channel in December and eat
returns in January. In every case the metric was a reasonable proxy right up until it became the
target, and then the measured number improved while the real thing decayed. Baseball is not exempt: a
hitter paid for OBP alone can learn to take walks in situations where swinging would win the game.</p>

<p>This is why choosing metrics is a management decision, not a reporting chore, and why the
professional habit is to pair every target with a counter-metric that catches the gaming: handle time
with resolution rate, units shipped with returns. Keep this section in mind for the Monday activity,
because your job there is to find one of these traps in the wild.</p>

<h2 id="s7"><span class="num">07</span>From the dugout to the dashboard</h2>

<p>What did the A's revolution look like as an information system? Unremarkably modest: public
statistics, DePodesta's laptop, and spreadsheet models. The lesson is not the technology; it is the
architecture, which is the same one every BI-capable business runs today, at larger scale.</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">The BI stack: operational systems, warehouse, dashboard</span>
<p>Operational systems, the registers and databases from Chapters 5 and 6, are built to record
transactions quickly, one at a time. Analysis asks the opposite kind of question: patterns across
millions of rows and months of history. So organizations copy operational data into a <strong>data
warehouse</strong>, a database organized for analysis rather than transactions, and put
<strong>dashboards</strong> on top: visual displays of the metrics that matter, updated continuously.
The separation exists so that a heavy analytical query never slows down the register, and so that
analysis runs on a cleaned, consistent copy, which after Labs 3 and 7 you know is not the copy the
registers write.</p></div>

<p>The last layer is <strong>self-service BI</strong>, tools like Tableau that let the analyst, rather
than a programmer, explore the warehouse and build the dashboard. That is this week's lab, and it
closes the loop on the course's longest-running thread. At Cascadia, revenue is the batting average:
Bellingham's looked fine on every standard report. The member attach rate is the on-base percentage:
the truer measure of the underlying engine, and the number that finally exposed the problem. You found
it in a pivot table in Lab 5; this week you will make it impossible for a manager to miss, which is
what a dashboard is for.</p>

<div class="callout"><strong>The one-sentence version</strong>
<p>BI is not having data. Everyone has data. BI is choosing the measure that tracks what you actually
care about, and putting it where decisions get made.</p></div>

<h2 id="s8"><span class="num">08</span>The other side: being measured</h2>

<p>The Moneyball story has winners it celebrates and costs it mentions quietly. The A's model worked
partly by overruling scouts, professionals with decades of pattern-recognition that resisted
quantification, and the analytics wave that followed thinned their ranks across the sport. Players
experienced the shift too: to a model you are a row of numbers, and the qualities the numbers do not
capture, leadership, resilience, how you play hurt, stop being priced. Some of that was the point;
prejudice about how an athlete looked was exactly the noise OBP filtered out. But a measurement regime
always sees some things by going blind to others, and the people inside it feel the blindness.</p>

<p>Two honest footnotes belong in the case. The 2002 A's, for all 103 wins, lost in the first playoff
round, and Beane's Oakland teams never won a World Series: analytics bought an edge, not a
championship, and edges decay. And once every team adopted the same methods, the advantage flowed back
to the largest payrolls, now spending efficiently. Measuring right is necessary. It is not, on its
own, sufficient, and it is never permanent. You will see the same pattern next week when every
retailer learns to mine its data and the question becomes who has more of it.</p>

<h2 id="s9"><span class="num">09</span>The five components of the 2002 A's</h2>

<table class="sumtable">
<tr><th>Component</th><th>In the case</th><th>The lesson</th></tr>
<tr><td><strong>Hardware</strong></td><td>A laptop and commodity computers; nothing exotic</td><td>The BI revolution was not a hardware story</td></tr>
<tr><td><strong>Software</strong></td><td>Spreadsheets and statistical models on public data</td><td>The model encodes the insight; the tool is replaceable</td></tr>
<tr><td><strong>Data</strong></td><td>A century of box scores every team also had</td><td>Advantage came from the question asked, not the data held</td></tr>
<tr><td><strong>Networks</strong></td><td>Published statistics, available to every rival</td><td>Shared data means information advantages are temporary</td></tr>
<tr><td><strong>People</strong></td><td>Beane choosing the model over a century of consensus</td><td>The scarce component was the willingness to trust a better measure</td></tr>
</table>

<h2 id="s10"><span class="num">10</span>Summary and vocabulary</h2>

<table class="sumtable">
<tr><th>Idea</th><th>This chapter's version</th><th>Where you meet it next</th></tr>
<tr><td><strong>Four kinds of analytics</strong></td><td>Descriptive to prescriptive; each rung changes decisions, not reports</td><td><a href="lab6-tableau.html">Lab 6's dashboard</a></td></tr>
<tr><td><strong>Proxy metrics</strong></td><td>Batting average vs. OBP; revenue vs. attach rate</td><td>The co-op memo, and every KPI you ever inherit</td></tr>
<tr><td><strong>Market inefficiency</strong></td><td>A mismeasured quality is a mispriced asset</td><td>Ch 2's five forces, revisited with data</td></tr>
<tr><td><strong>Goodhart's law</strong></td><td>Targets corrupt their own measures</td><td>The Monday activity</td></tr>
<tr><td><strong>The BI stack</strong></td><td>Operational systems feed a warehouse; dashboards sit on top</td><td>Cloud warehouses, Week 10</td></tr>
</table>

<dl class="vocab">
<div><dt>Business intelligence (BI)</dt><dd>Systems and practices that turn organizational data into decision-ready information.</dd></div>
<div><dt>Descriptive / diagnostic / predictive / prescriptive</dt><dd>The four kinds of analytics: what happened, why, what will, what to do.</dd></div>
<div><dt>Metric / KPI</dt><dd>A number chosen to stand for something the business cares about; a key performance indicator is a metric elevated to a target.</dd></div>
<div><dt>Proxy</dt><dd>What every metric secretly is: a stand-in for the real thing, valid only as far as it tracks it.</dd></div>
<div><dt>Measurement validity</dt><dd>Whether a metric actually measures what it claims to.</dd></div>
<div><dt>Sabermetrics</dt><dd>The empirical analysis of baseball; the movement that found the industry's measurement error.</dd></div>
<div><dt>On-base percentage</dt><dd>Share of plate appearances reaching base; the undervalued, more valid measure.</dd></div>
<div><dt>Market inefficiency</dt><dd>A gap between price and value, here created by an industry-wide measurement error.</dd></div>
<div><dt>Correlation vs. causation</dt><dd>Moving together vs. one driving the other; trust correlations with a mechanism and a large sample.</dd></div>
<div><dt>Small-sample problem</dt><dd>Patterns in little data mislead; a five-game series is a coin flip.</dd></div>
<div><dt>Goodhart's law</dt><dd>When a measure becomes a target, it ceases to be a good measure.</dd></div>
<div><dt>Data warehouse</dt><dd>A database organized for analysis, fed by copies of operational data.</dd></div>
<div><dt>Dashboard / self-service BI</dt><dd>Visual metric displays, and the tools (like Tableau) that let analysts build them directly.</dd></div>
</dl>

<div class="tps">
  <div class="tps-head"><span>Monday activity &middot; A metric that made a business worse</span><span class="mins">20 minutes</span></div>
  <div class="tps-body">
    <p class="tps-setup">Every organization you have ever worked for, bought from, or studied in runs
    on metrics, and somewhere in it, right now, a reasonable-looking number is being optimized at the
    expense of the thing it was supposed to measure. Wait times, ticket counts, grades, engagement,
    units, stars.</p>
    <div class="tps-q"><p>Name one metric, from a job, a business you know, or this university, that is actively making the real goal worse. What is the real goal, and how does optimizing the number damage it?</p></div>
    <div class="tps-steps">
      <div class="tps-step"><div class="ph">Think <span>3 min</span></div><p>Pick your metric and write the gap: the number says X is improving while the real thing does Y.</p></div>
      <div class="tps-step"><div class="ph">Pair <span>5 min</span></div><p>Trade examples, then design the fix for your partner's case: a counter-metric that would catch the gaming.</p></div>
      <div class="tps-step"><div class="ph">Share <span>12 min</span></div><p>We will collect the examples on the board and sort them: proxies that drifted, targets that got gamed, and samples too small to trust.</p></div>
    </div>
    <div class="tps-note"><strong>Where this lands</strong>Every example on the board is Goodhart's law wearing different clothes, and every fix is the same move the A's made: ask what the number is a proxy for, and measure closer to the real thing. That question is the whole chapter, and on Thursday you will point a dashboard at it.</div>
  </div>
</div>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach and sparring partner</strong>
  <p>Have an AI quiz you on the four kinds of analytics with fresh business examples until you can
  classify them cold, or argue your discussion-question position against it, your position first, per
  the Lab 1 rules. One warm-up worth doing: ask it to name three proxy metrics in an industry you care
  about, then judge for yourself which would survive this chapter's validity test.</p></div>
</div>

<h2 id="questions"><span class="num">11</span>Discussion questions</h2>
<p><em>Groups of three for Wednesday; each group takes one and presents.</em></p>
<ol class="dq">
<li>Make the best case that batting average was a <em>reasonable</em> metric for a century, then explain what changed. Was the industry stupid, or was the metric serving a purpose other than predicting wins?<span class="tag tag-open">Judgment</span></li>
<li>The A's advantage came from better measurement of public data, and it decayed within a few years. Using Chapter 2's five forces, explain why information advantages erode faster than most, and name one kind that erodes slowly.<span class="tag tag-open">Connect</span></li>
<li>Find the OBP of another industry: a widely used headline metric with weak validity, and the better measure hiding in the same data. Defend your pick. (Followers, box office, GPA, and steps counted are all fair game.)<span class="tag tag-warm">Apply</span></li>
<li>Give a real example of Goodhart's law from your own work, school, or consumer life, and design the counter-metric that would catch the gaming without creating a new target to game.<span class="tag tag-hard">Design</span></li>
<li>Beane said his approach could not be counted on in a five-game series. A startup founder tells you their product works because sales doubled last month. Write the three questions this chapter trains you to ask before believing either claim.<span class="tag tag-open">Analyze</span></li>
<li>At Cascadia, revenue was the batting average and attach rate was the OBP. Propose one more metric the co-op should track that no standard retail report includes, and say what decision it would change.<span class="tag tag-warm">Apply</span></li>
<li>The analytics wave displaced scouts whose expertise resisted quantification. When should an organization trust the model over the expert, and when the reverse? Give one rule, not a platitude, and stress-test it against both the A's and a hospital.<span class="tag tag-hard">Judgment</span></li>
<li>Your Lab 6 dashboard, like every dashboard, has a blind spot: something about the co-op it cannot reveal. Name it, and say what it would take to see it.<span class="tag tag-open">Reflect</span></li>
</ol>

<h2><span class="num">12</span>Sources and further reading</h2>
<ul class="sources">
<li>Michael Lewis, <em>Moneyball: The Art of Winning an Unfair Game</em> (W. W. Norton, 2003): the original account of the 2002 season, Beane, DePodesta, and the sabermetric argument.</li>
<li>Baseball-Reference, 2002 Oakland Athletics season page: the record (103&ndash;59), the August 13 to September 4 winning streak, and player statistics including Hatteberg's .374 OBP.</li>
<li>Contemporary payroll reporting (USA Today MLB salary database, 2002): Oakland at roughly $41 million, third lowest; the Yankees at roughly $125 million.</li>
<li>Bill James, <em>Baseball Abstract</em> series: the sabermetric analyses, published for two decades before any team acted on them, a useful case in how long an industry can ignore valid measurement.</li>
</ul>

<p style="margin-top:2.5rem"><a href="lab6-tableau.html">Lab 6, Data Visualization with Tableau, runs this week &#8594;</a></p>

''' + TAIL
open('chapter7-moneyball.html','w').write(CH7)
print('chapter7-moneyball.html:', len(CH7))

# ============================================================ CHAPTER 8
CH8 = make_head("Chapter 8: AI, Machine Learning &amp; Bias",
 "Amazon's scrapped hiring model, the recommendation engine built from the same math, predictive policing's feedback loop, and Spotify's 1.4 billion LLM-written Wrapped reports.", 'ch8')

CH8 += '''<main class="chapwrap">

<header class="chaphead">
  <p class="eyebrow">Chapter 8 &middot; AI, Machine Learning &amp; Bias</p>
  <h1>AI and Machine Learning: When the Model Learns the Wrong Lesson</h1>
  <p class="anchor">Machine learning is the most consequential business technology of your working
  lifetime: it flags fraud before your card is charged, folds proteins that won a Nobel Prize, powers
  the recommendations behind a third of Amazon's sales, and wrote 1.4 billion Wrapped stories last
  year. And in 2015, the same math taught an Amazon hiring engine to prefer men. This chapter is
  about what machine learning actually is, why one idea produces both outcomes, and how the people
  who run these systems, not the systems themselves, determine which one you get.</p>
  <div class="meta-row">
    <span>Cases: Amazon (2014&ndash;18) &middot; Spotify Wrapped Archive (2025)</span>
    <span class="alt">Week 10 &middot; Monday</span>
    <span class="alt"><a href="schedule.html" style="color:inherit;text-decoration:none">Wednesday: what computing costs &#8594;</a></span>
  </div>
</header>

<div class="statrow">
  <div class="stat"><b>10 yrs</b><span>of past resumes as training data</span></div>
  <div class="stat"><b>1&ndash;5</b><span>stars per applicant, like a product</span></div>
  <div class="stat"><b>2017</b><span>the year Amazon killed the project</span></div>
  <div class="stat"><b>1.4B</b><span>LLM-written Wrapped reports, pre-generated</span></div>
  <div class="stat"><b>~350M</b><span>Spotify users served in one launch</span></div>
</div>

<div class="toc"><strong>Contents</strong>
<a href="#s1">1. The machine that did not like women</a>
<a href="#s2">2. What AI actually is</a>
<a href="#s3">3. How a model learns</a>
<a href="#s4">4. The same math that makes money</a>
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
<tr><td class="t">0:00</td><td class="w">Open</td><td>Read the hook cold: Amazon built an engine to rate job applicants one to five stars, like products. Ask the room what could go wrong, and collect guesses on the board before revealing that the engine's own builders found the answer.</td></tr>
<tr><td class="t">0:05</td><td class="w">Lecture</td><td>What ML is: patterns learned from data, not rules written by hand. Walk the resume tool as the anatomy of supervised learning, then flip the coin: the same math flags fraud, folds proteins, and drives a third of Amazon's sales. The symmetry is the lecture; students should leave impressed by the technology and skeptical of unexamined training data, in that order.</td></tr>
<tr><td class="t">0:35</td><td class="w">Lecture</td><td>Bias in, bias out, and the feedback loop: the "women's" penalty, why editing terms out could not fix it, then predictive policing as the case where the model's output writes its own future training data.</td></tr>
<tr><td class="t">0:50</td><td class="w">Think-pair-share</td><td>The tool works; now what? See the activity below.</td></tr>
<tr><td class="t">1:10</td><td class="w">Close</td><td>Wrapped Archive in five minutes: 1.4 billion grounded LLM reports, and Spotify's own engineers saying the model call was the easy part. It bridges directly to Wednesday: all of this runs on hardware somebody pays for.</td></tr>
</table></div>

<h2 id="s1"><span class="num">01</span>The machine that did not like women</h2>

<p>The idea was reasonable, even obvious. Amazon receives a flood of resumes, automation is the
company's core competency, and hiring is expensive and slow. So, beginning in 2014, a team in
Edinburgh built experimental models to do for recruiting what the company had done for retail: read
each incoming resume and score the applicant from one to five stars. One insider described the dream
to Reuters: give the engine one hundred resumes, it spits out the top five, you hire those.</p>

<p>To learn what a strong applicant looked like, the models were trained on the resumes the company
had received over the previous ten years, together with how those candidacies had turned out. And
here is the whole story in one sentence: <strong>the tech industry's past applicants were mostly men,
so the model learned that resumes resembling men's resumes were what success looked like.</strong> By
2015 the team found the system penalizing resumes containing the word "women's", as in "women's chess
club captain", and downgrading graduates of two all-women's colleges, while favoring verbs that
happened to be more common on male engineers' resumes, like "executed" and "captured".</p>

<p>Amazon edited the model to neutralize those specific terms, then confronted the harder truth: there
was no way to be confident it had not found other, subtler proxies for gender. The company lost
confidence in the project and shut it down, telling Reuters the tool was never used by recruiters to
evaluate candidates. Hold on to the shape of this failure, because nobody wrote a biased rule. Nobody
wrote any rule. That is precisely what machine learning means, and it is where this chapter starts.</p>

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
someone can find and fix. A learned system does what its data taught it, its reasoning is not written
down anywhere a manager can read, and a bad outcome traces to the examples it was fed, which is why
the rest of this chapter is mostly about data, not algorithms.</p>

<h2 id="s3"><span class="num">03</span>How a model learns</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Training data, labels, and supervised learning</span>
<p>The workhorse of business ML is <strong>supervised learning</strong>: you assemble
<strong>training data</strong>, historical examples, each carrying a <strong>label</strong>, the
outcome you want predicted, and the model adjusts itself until its predictions match the labels. Then
comes <strong>inference</strong>: showing the trained model new, unlabeled cases and using its
predictions. Amazon's tool is a textbook specimen. Examples: a decade of resumes, represented as
tens of thousands of terms. Labels: how each candidacy fared. Prediction: a one-to-five score for a
new resume. The model did exactly what supervised learning does, faithfully. The labels were the
problem, because the labels were history, and history had a skew.</p></div>

<p>Its sibling, <strong>unsupervised learning</strong>, finds structure in data with no labels at
all, like clustering the co-op's members into natural segments nobody predefined. Keep one idea from
this section above all: <em>a supervised model is a machine for making the future resemble the
labeled past.</em> When the past is what you want more of, that is a superpower. When it is not, the
model automates the very pattern you were hoping to escape.</p>

<h2 id="s4"><span class="num">04</span>The same math that makes money</h2>

<p>It would be easy to file the hiring tool under "AI gone wrong" and move on. The more instructive
fact is that the identical approach, pointed at products instead of people, is one of the most
successful business systems ever built. Amazon's recommendation engine, the "customers who bought
this also bought" machinery, runs on <strong>collaborative filtering</strong>: learning patterns from
millions of past purchases to predict what you will want next. Amazon's engineers published the core
method, item-to-item collaborative filtering, back in 2003, and a widely cited McKinsey estimate has
put roughly 35 percent of Amazon's sales behind its recommendations. The same learned-pattern
machinery drives the demand forecasts that decide what sits in which warehouse before you order it.</p>

<p>And Amazon is one entry in a long ledger. The same learned-pattern machinery flags credit-card
fraud in the milliseconds between swipe and approval, which is why your bank texts you about a
suspicious charge before you have left the store. In medicine, models trained on labeled scans have
matched specialist performance at detecting diabetic retinopathy and certain cancers in published
studies, extending screening to clinics that have no specialist. DeepMind's AlphaFold predicted the
three-dimensional structure of essentially every known protein, work that earned a share of the 2024
Nobel Prize in Chemistry and compressed what had been months of laboratory effort per protein into
minutes. Machine translation and speech recognition, both supervised learning at heart, have quietly
become accessibility infrastructure for hundreds of millions of people. None of this is hype; it is
deployed, audited, and paying for itself, and it is the reason every serious company is asking where
learned prediction fits in its own operations, a question someone with your degree will be in the
room for.</p>

<p>So the resume tool was not a rogue experiment by people who misunderstood the company. It was the
company's most proven idea, applied one domain too far. That is the honest frame for AI in business:
the technology is domain-blind. It predicts hits from history with equal confidence whether the
history is shopping carts or hiring decisions, and whether repeating that history is profitable,
harmless, or illegal. The math does not know the difference. Someone in the room has to, and this
course exists partly so that someone can be you.</p>

<div class="pull"><p>The model that recommends your next purchase and the model that rejected her resume are the same idea. Only the training data differs.</p></div>

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

<p>The resume tool at least learned from a fixed past. A nastier structure appears when a model's
outputs generate its future training data. <strong>Predictive policing</strong> systems, adopted by
police departments over the last decade, forecast where crime is likeliest and route patrols there.
Send more patrols to a neighborhood and they observe more offenses there, which enters the data as
more recorded crime, which raises the model's forecast, which sends more patrols. The model's
prediction manufactures its own confirmation, and historical over-policing hardens into
mathematically laundered permanent policy.</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Feedback loops</span>
<p>A <strong>feedback loop</strong> exists when a system's outputs alter the inputs it will learn
from next. Recommendation engines have gentle ones: recommend a song, it gets played, plays justify
recommending it. Predictive systems that direct real-world action, patrols, loans, audits, hiring,
have consequential ones, because the model changes the world that generates its evidence. The test to
carry into any AI deployment: <em>does acting on this prediction change the data that will judge the
prediction?</em> If yes, the model can be confidently, self-certifyingly wrong.</p></div>

<h2 id="s7"><span class="num">07</span>Generative AI at 1.4 billion</h2>

<p>Now the current generation, at industrial scale, through a system you have been studying all
quarter. In Week 1 Spotify Wrapped was your "what is MIS" specimen; in Lab 7 you learned its core is
a GROUP BY. For Wrapped 2025, Spotify added an <strong>Archive</strong>: for each of roughly 350
million eligible users, heuristics scanned the year's listening for up to five "remarkable days",
your biggest discovery day, your most nostalgic day, and a language model wrote a short personalized
narrative about each. About 1.4 billion reports, all pre-generated before launch day, each one a call
to a model Spotify fine-tuned and distilled to make the cost survivable.</p>

<p>Two engineering choices carry the lesson. First, <strong>grounding</strong>: every narrative was
generated from the user's actual listening records, passed into the prompt, because an ungrounded
LLM will cheerfully invent a touching day you never had. That failure mode has a name you met in Lab
1, <strong>hallucination</strong>, and the calculator test you passed there, the confident wrong
total, is the same phenomenon at desk scale. Second, evaluation at volume: no human can read 1.4
billion reports, so Spotify used an LLM as an automated judge on a sample of about 165,000, which is
how they caught, among other things, a timezone bug attributing plays to the wrong day, before users
saw it. Their engineers' own summary of the project is the chapter's thesis in one line: at this
scale, <em>the LLM call is the easy part</em>. The system around it, the data pipeline, the
grounding, the evaluation, the capacity planning, is the achievement, and every word of that sentence
describes MIS work, not model-building work.</p>

<h2 id="s8"><span class="num">08</span>What business people do with AI</h2>

<p>As with security in Chapter 9, students assume AI jobs are engineering jobs they are unqualified
for, and as with security, the decisions that determine outcomes are mostly business decisions. The
roles a business graduate actually fills:</p>

<p><strong>Evaluation and audit.</strong> Somebody decided to test whether the resume tool was
gender-neutral, and somebody designed Spotify's judge-and-sample scheme. Deciding what "working
correctly" means for a model, and how you would know, is analytical work built on exactly the
measurement-validity thinking of Chapter 7: an unmeasured model is an unmanaged one.</p>

<p><strong>Human-in-the-loop design.</strong> Deciding which decisions a model may make alone, which
require a human to confirm, and which a model may only inform. You have run this discipline on
yourself since Lab 1; designing it for an organization is the same three lights, drawn as policy.</p>

<p><strong>AI governance.</strong> The Chapter 10 apparatus, applied here: who owns each model, what
data it may train on, what it must never be used for, and who answers when it fails. The EU and a
growing list of US states now regulate automated hiring tools specifically because of cases like
Amazon's, so this is compliance work with a hard legal edge, not a philosophy seminar.</p>

<p><strong>Vendor and use-case selection.</strong> Most companies will buy AI, not build it, which
makes "which model, whose cloud, at what cost, for which process" a procurement-and-strategy question,
one Wednesday's chapter prices out in detail.</p>

<h2 id="s9"><span class="num">09</span>The other side: the people in the data</h2>

<p>Every system in this chapter runs on data generated by people who never signed up to be training
examples. The applicants in Amazon's ten years of resumes were job-seekers, not volunteers for an
experiment that would score people like them. The residents of a heavily patrolled neighborhood never
agreed to have their arrest records forecast their children's police coverage. Spotify's Archive drew
on years of retained listening history, and thoughtful engineering coverage of the launch raised
exactly that question: delight built on how much a platform remembers about you. This is Chapter 10's
"data about people who never agreed", resurfacing one layer up the stack.</p>

<p>Behind the models sits labor the demos never show: data-labeling workers, often contractors in
lower-wage countries, tagging the examples supervised learning requires, including the disturbing
content that moderation models train on. And generative AI produces its own pollution for other
people to absorb: Spotify itself reported removing some 75 million spam and AI-generated tracks in
2025 to protect artists and royalties, the same company using LLMs as a feature while fighting them
as an infestation. When a company weighs an AI deployment, most of these costs sit off its books, an
externality, which is the same reason Chapter 9 gave for why security cannot be left to private
cost-benefit math alone.</p>

<h2 id="s10"><span class="num">10</span>The five components of a machine-learning system</h2>

<table class="sumtable">
<tr><th>Component</th><th>In these cases</th><th>The lesson</th></tr>
<tr><td><strong>Hardware</strong></td><td>The compute behind training and 1.4 billion generations</td><td>Model appetite is a hardware bill; Wednesday prices it</td></tr>
<tr><td><strong>Software</strong></td><td>The models, and the pipelines that ground and evaluate them</td><td>The model is a component; the system is the achievement</td></tr>
<tr><td><strong>Data</strong></td><td>Ten years of resumes; a year of listening; arrest records</td><td>Training data is the system's memory of the past, skew included</td></tr>
<tr><td><strong>Networks</strong></td><td>Serving 350 million users in one coordinated launch</td><td>Scale is a distribution problem before it is an AI problem</td></tr>
<tr><td><strong>People</strong></td><td>Choosing the training data, testing for bias, killing the tool</td><td>Every consequential choice in this chapter was a human one</td></tr>
</table>

<h2 id="s11"><span class="num">11</span>Summary and vocabulary</h2>

<table class="sumtable">
<tr><th>Idea</th><th>This chapter's version</th><th>Where you meet it next</th></tr>
<tr><td><strong>The upside is real</strong></td><td>Fraud flags, folded proteins, screening where no specialist works</td><td>The AI decisions your first employer is making now</td></tr>
<tr><td><strong>Learning vs. rules</strong></td><td>Behavior comes from training data, not stated intentions</td><td>Every AI headline you read after this course</td></tr>
<tr><td><strong>Bias in, bias out</strong></td><td>The "women's" penalty nobody wrote</td><td><a href="chapter10-equifax.html">Ch 10's accountability question</a></td></tr>
<tr><td><strong>Feedback loops</strong></td><td>Predictions that manufacture their own confirmation</td><td>The Monday activity's hardest cases</td></tr>
<tr><td><strong>Grounding vs. hallucination</strong></td><td>1.4 billion reports tied to real listening data</td><td><a href="lab1-genai.html">Lab 1's calculator test</a>, which you already passed</td></tr>
<tr><td><strong>The system, not the model</strong></td><td>"The LLM call is the easy part"</td><td>Wednesday: the cloud it all runs on</td></tr>
</table>

<dl class="vocab">
<div><dt>Artificial intelligence</dt><dd>Computers doing tasks that seem to require intelligence; today, mostly via machine learning.</dd></div>
<div><dt>Machine learning</dt><dd>Learning patterns from examples instead of following hand-written rules.</dd></div>
<div><dt>Training data / label</dt><dd>The historical examples a model learns from, and the outcome attached to each.</dd></div>
<div><dt>Supervised / unsupervised</dt><dd>Learning from labeled outcomes vs. finding structure with no labels.</dd></div>
<div><dt>Inference</dt><dd>Using the trained model on new cases; where models earn their keep.</dd></div>
<div><dt>Collaborative filtering</dt><dd>Predicting what you will want from patterns across everyone's past behavior; the recommendation engine's core.</dd></div>
<div><dt>Training-data bias</dt><dd>A skew in the examples, faithfully learned and reproduced.</dd></div>
<div><dt>Proxy discrimination</dt><dd>The model rediscovering a removed attribute through its correlates.</dd></div>
<div><dt>Feedback loop</dt><dd>Outputs that shape the future training data, letting a model confirm itself.</dd></div>
<div><dt>Generative AI / LLM</dt><dd>Models that produce new content; large language models are the text-generating kind.</dd></div>
<div><dt>Fine-tuning / distillation</dt><dd>Adapting a model to a task, and compressing a large one into a cheaper one that keeps what matters.</dd></div>
<div><dt>Grounding</dt><dd>Tying generated output to verified data so the model narrates reality instead of inventing it.</dd></div>
<div><dt>Hallucination</dt><dd>Fluent, confident output that is simply wrong; Lab 1's calculator test at scale.</dd></div>
<div><dt>Human-in-the-loop</dt><dd>Deciding which model outputs require a person's judgment before they act on the world.</dd></div>
</dl>

<div class="tps">
  <div class="tps-head"><span>Monday activity &middot; The tool works. Now what?</span><span class="mins">20 minutes</span></div>
  <div class="tps-body">
    <p class="tps-setup">It is 2015 and you run recruiting technology at Amazon. The engine is fast,
    the top-five lists look plausible, and it would save thousands of screening hours a year. Your ML
    team has just shown you the finding: it penalizes the word "women's", and they can edit that term
    out but cannot promise there are no subtler proxies among fifty thousand others.</p>
    <div class="tps-q"><p>Kill it, fix it, or keep it with a human reviewing every recommendation? Commit to one, and name the single condition that would have to be true for a model to ever touch a hiring decision.</p></div>
    <div class="tps-steps">
      <div class="tps-step"><div class="ph">Think <span>3 min</span></div><p>Choose, and write your condition as a testable sentence, something an auditor could check, not a vibe.</p></div>
      <div class="tps-step"><div class="ph">Pair <span>5 min</span></div><p>Find someone who chose differently. Attack each other's condition: what failure slips through it?</p></div>
      <div class="tps-step"><div class="ph">Share <span>12 min</span></div><p>We will sort the conditions on the board into measurable ones and unmeasurable ones, and notice which pile "a human reviews it" lands in once you ask what the human actually checks.</p></div>
    </div>
    <div class="tps-note"><strong>Where this lands</strong>Amazon chose kill, and the reasoning generalizes: a model you cannot evaluate is a model you cannot deploy, whatever it saves. "Human in the loop" is a real answer only when the human has the information, time, and authority to overrule the machine, otherwise it is a rubber stamp with a pulse. The measurable-condition habit is the one to keep; it is Chapter 7's validity question, aimed at AI.</div>
  </div>
</div>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach and sparring partner</strong>
  <p>Fitting week for it: have an AI quiz you on this vocabulary, then run one live experiment on the
  chapter's own subject. Ask it a question about your hometown or a hobby you know deeply, and audit
  the answer for confident errors. You are performing evaluation, Section 8's first job, on the tool
  itself. One standing rule extends the red light from Lab 1: never paste real people's personal or
  identifying data, resumes included, into an AI tool. You would be adding them to somebody's
  training data, which after this chapter needs no further explanation.</p></div>
</div>

<h2 id="questions"><span class="num">12</span>Discussion questions</h2>
<p><em>Groups of three; each group takes one and reports out.</em></p>
<ol class="dq">
<li>An executive says: "We should trust the model precisely because it has no prejudices; it is just math." Using the resume case, explain what this gets right and where it fatally goes wrong.<span class="tag tag-open">Explain</span></li>
<li>Design the audit that would have caught the resume tool before launch: what would you test, against what data, and what result would trigger a kill decision? Be concrete enough that an engineer could run it.<span class="tag tag-hard">Design</span></li>
<li>Amazon scrapped the tool. Argue the opposite case, that fixing and shipping it with safeguards was the better call, then say which argument wins and why.<span class="tag tag-open">Evaluate</span></li>
<li>Find a feedback loop in a domain other than policing, somewhere a prediction changes the data that will later judge it. Loan approvals, school rankings, and content moderation are all candidates. Trace one full lap of your loop.<span class="tag tag-warm">Apply</span></li>
<li>What stops Wrapped Archive from telling you about a moving listening day you never had? Name the engineering choice, connect it to Lab 1's calculator test, and say what the equivalent safeguard would be for an AI that answers customer-service questions.<span class="tag tag-open">Connect</span></li>
<li>This chapter passed along a widely cited estimate that recommendations drive roughly 35 percent of Amazon's sales. Treat that number with Chapter 7's skepticism: what would you need to know before repeating it in a board memo?<span class="tag tag-warm">Analyze</span></li>
<li>Section 9 argues AI's costs, scored applicants, labeling labor, AI-generated spam, largely sit off the deploying company's books. Make the strongest case that market pressure will discipline AI use without regulation, then the strongest case that it will not, and note where you saw this exact argument before.<span class="tag tag-hard">Judgment</span></li>
<li>Write the one-sentence rule for when a human must stay in the loop of an automated decision, then stress-test your sentence against three cases: a product recommendation, a resume screen, and a medical triage suggestion. Does it survive all three?<span class="tag tag-hard">Design</span></li>
</ol>

<h2><span class="num">13</span>Sources and further reading</h2>
<ul class="sources">
<li>Jeffrey Dastin, Reuters, <em>Amazon scraps secret AI recruiting tool that showed bias against women</em> (October 2018): the original report; the training data, the "women's" penalty, the two colleges, the favored verbs, and Amazon's statement that the tool never evaluated real candidates.</li>
<li>MIT Technology Review, <em>Amazon ditched AI recruitment software because it was biased against women</em> (October 2018): a concise account of why term-level fixes could not restore confidence in neutrality.</li>
<li>Greg Linden, Brent Smith, and Jeremy York, <em>Amazon.com Recommendations: Item-to-Item Collaborative Filtering</em>, IEEE Internet Computing (2003): the recommendation engine's core method, published by its builders.</li>
<li>Spotify Engineering, <a href="https://engineering.atspotify.com/2026/3/inside-the-archive-2025-wrapped">Inside the Archive: The Tech Behind Your 2025 Wrapped Highlights</a> (2026): the remarkable-days heuristics, the ~1.4 billion pre-generated reports for ~350 million users, the fine-tuned and distilled model, and the LLM-as-judge evaluation on a ~165,000-report sample.</li>
<li>The McKinsey figure attributing roughly 35 percent of Amazon's sales to recommendations is a widely circulated 2013 estimate, not an Amazon disclosure; Discussion question 6 asks you to treat it accordingly.</li>
</ul>

<p style="margin-top:2.5rem"><a href="schedule.html">Wednesday: cloud, data centers, and what computing costs &#8594;</a></p>

''' + TAIL
open('chapter8-ai-ml.html','w').write(CH8)
print('chapter8-ai-ml.html:', len(CH8))

# ============================================================ site-wide nav
OLD_CH6 = '<a href="chapter6-nike-sap.html"><span class="lbl">Chapter 6 &middot; Week 7</span>Enterprise Systems &mdash; Nike/SAP</a>'
NEW_CH678 = OLD_CH6 + '''
      <a href="chapter7-moneyball.html"><span class="lbl">Chapter 7 &middot; Week 6</span>Business Intelligence &mdash; Moneyball</a>
      <a href="chapter8-ai-ml.html"><span class="lbl">Chapter 8 &middot; Week 10</span>AI, Machine Learning &amp; Bias &mdash; Amazon</a>'''
OLD_SOON = '<a class="soon" href="#"><span class="lbl">Chapters 7&ndash;8, 11&ndash;12</span>BI, AI/ML, Cloud, IoT (in progress)</a>'
NEW_SOON = '<a class="soon" href="#"><span class="lbl">Chapters 11&ndash;12</span>Cloud, IoT (in progress)</a>'

for fn in glob.glob('*.html'):
    t = open(fn).read(); orig = t
    cur_ch6 = OLD_CH6.replace('<a href', '<a class="current" href')
    if cur_ch6 in t:   # chapter6's own page marks itself current
        t = t.replace(cur_ch6, NEW_CH678.replace('<a href="chapter6-nike-sap.html">',
                                                 '<a class="current" href="chapter6-nike-sap.html">'))
    else:
        t = t.replace(OLD_CH6, NEW_CH678)
    t = t.replace(OLD_SOON, NEW_SOON)
    t = t.replace('<a href="%s">' % fn, '<a class="current" href="%s">' % fn)
    if t != orig:
        open(fn,'w').write(t); print('nav updated:', fn)

# ============================================================ schedule links
s = open('schedule.html').read()
s = s.replace('<h4 class="pending">Business intelligence and analytics<span class="pill wip">Chapter in progress</span></h4>',
              '<h4><a href="chapter7-moneyball.html">Business intelligence and analytics</a></h4>')
s = s.replace('<h4 class="pending">Moneyball / Oakland A\'s</h4>',
              '<h4><a href="chapter7-moneyball.html">Moneyball / Oakland A\'s</a></h4>')
s = s.replace('<h4 class="pending">AI, machine learning, and bias<span class="pill wip">Chapter in progress</span></h4>',
              '<h4><a href="chapter8-ai-ml.html">AI, machine learning, and bias</a></h4>')
open('schedule.html','w').write(s)
print('schedule linked')
