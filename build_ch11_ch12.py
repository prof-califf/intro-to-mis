"""Builds chapter11-software.html and chapter12-cloud.html from the ch9 shell.
The book's chapter slate is complete after this: 0-12, no gaps announced.
Also updates nav site-wide (removes the 'in progress' chapters line), the
schedule links, Chapter 8's forward links, and the index cards."""
import re, glob

ch9 = open('chapter9-changehealthcare.html').read()
HEAD = ch9[:ch9.index('<main class="chapwrap">')]
TAIL = ch9[ch9.index('</main>'):]

def make_head(title, desc):
    h = HEAD
    h = re.sub(r'<title>[^<]*</title>', '<title>%s | MIS 320</title>' % title, h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="%s">' % desc, h, count=1)
    h = h.replace('class="current" href="chapter9-changehealthcare.html"', 'href="chapter9-changehealthcare.html"')
    return h

# ============================================================ CHAPTER 11
CH11 = make_head("Chapter 11: Software Design &amp; Selection: Robles v. Domino's",
 "A blind man, a screen reader, and a pizza he could not order: usability, accessibility, the ADA online, and how businesses actually choose software.")

CH11 += '''<main class="chapwrap">

<header class="chaphead">
  <p class="eyebrow">Chapter 11 &middot; Software Design &amp; Selection</p>
  <h1>Software: The Pizza You Could Not Order</h1>
  <p class="anchor">Guillermo Robles is blind and uses screen-reading software that speaks a website
  aloud. At least twice, he tried to order a customized pizza from Domino's, on the website and in
  the app, and could not, because neither was built to work with a screen reader. In 2016 he sued,
  and the case climbed all the way to the Supreme Court's doorstep. This chapter is about the two
  software decisions every business makes, how it is designed and how it is chosen, and why the
  interface is not decoration: it is the part of the system that decides who gets to be a customer.</p>
  <div class="meta-row">
    <span>Case: Robles v. Domino's Pizza (2016&ndash;2022)</span>
    <span class="alt">Week 9 &middot; Wednesday (Monday is Exam 2)</span>
    <span class="alt"><a href="schedule.html" style="color:inherit;text-decoration:none">Paired lab: UX Design (Lab 9) &#8594;</a></span>
  </div>
</header>

<div class="statrow">
  <div class="stat"><b>2</b><span>channels that failed him: website and app</span></div>
  <div class="stat"><b>2016</b><span>the lawsuit, filed over an unorderable pizza</span></div>
  <div class="stat"><b>2019</b><span>Ninth Circuit: the ADA applies online</span></div>
  <div class="stat"><b>1990</b><span>the ADA, written before the web existed</span></div>
  <div class="stat"><b>1,000s</b><span>of web-accessibility suits now filed each year</span></div>
</div>

<div class="toc"><strong>Contents</strong>
<a href="#s1">1. The pizza that would not order</a>
<a href="#s2">2. Software, sorted</a>
<a href="#s3">3. The interface decides who gets in</a>
<a href="#s4">4. Accessibility is not a feature request</a>
<a href="#s5">5. The case: the ADA meets the web</a>
<a href="#s6">6. How businesses choose software</a>
<a href="#s7">7. Build, buy, or subscribe</a>
<a href="#s8">8. The other side: who software forgets</a>
<a href="#s9">9. The five components</a>
<a href="#s10">10. Summary and vocabulary</a>
<a href="#questions">11. Discussion questions</a>
</div>

<div class="plan">
<div class="plan-head">Wednesday session plan &middot; 80 minutes &middot; the post-exam session, so it opens gently</div>
<table>
<tr><td class="t">0:00</td><td class="w">Open</td><td>Ask everyone to close their eyes and order a pizza in their head using only what a screen reader would speak aloud. Then play or read thirty seconds of a screen reader on a cluttered site. The room understands the case before you state it.</td></tr>
<tr><td class="t">0:05</td><td class="w">Lecture</td><td>The Robles story, then the sorting: system versus application software, custom versus packaged versus SaaS, and usability as measurable properties, not taste.</td></tr>
<tr><td class="t">0:30</td><td class="w">Lecture</td><td>The legal arc: district court, Ninth Circuit, cert denied, and what "no regulations yet is not no obligation" means, an echo of the Chapter 8 governance principle. Then software selection: requirements, scripted demos, TCO, and accessibility as an RFP line.</td></tr>
<tr><td class="t">0:55</td><td class="w">Think-pair-share</td><td>Pick a point-of-sale system for Cascadia. See the activity below.</td></tr>
<tr><td class="t">1:15</td><td class="w">Close</td><td>Preview Lab 9: they will test real interfaces the way Robles experienced them, and redesign what fails.</td></tr>
</table></div>

<h2 id="s1"><span class="num">01</span>The pizza that would not order</h2>

<p>Domino's, the company from Chapter 3, rebuilt itself as "a tech company that happens to sell
pizza," and by the mid-2010s a large share of its orders arrived through its website and app. That is
the front door Guillermo Robles walked up to. His screen reader converts on-screen text and controls
into speech, and it works only when software is built with the underlying labels and structure the
reader needs. Domino's site and app were not. On at least two occasions he could not complete an
order or claim an online-only discount, which meant the company's digital front door, its proudest
system, was closed to him. In September 2016 he sued under the Americans with Disabilities Act.</p>

<p>Domino's defense is worth stating fairly, because your discussion questions will ask you to weigh
it. The company argued that the ADA, a 1990 law about physical places of public accommodation, does
not reach websites and apps at all, that no federal regulations existed telling businesses what an
accessible website even is, and that Mr. Robles was not shut out of Domino's because he could always
order by phone. Keep those three arguments in mind; a federal appeals court is going to answer each
one, and the answers now bind every business with a website. But first, the concepts the case sits
on.</p>

<h2 id="s2"><span class="num">02</span>Software, sorted</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Kinds of software, and where software comes from</span>
<p><strong>System software</strong>, the operating systems and utilities that run the machine, versus
<strong>application software</strong>, the programs that do the business's actual work: a register, a
payroll system, a pizza-ordering app. Applications arrive three ways. <strong>Custom</strong>
software is built for you, fits exactly, and costs the most to create and maintain.
<strong>Packaged</strong> (off-the-shelf) software is bought and installed, cheaper, and fits
approximately, which is why Chapter 6 spent a whole case on the configure-versus-customize decision.
<strong>Software as a service (SaaS)</strong> is rented: it runs on the vendor's computers, you reach
it through a browser, and you pay by subscription. Most new business software today is SaaS, for
reasons the next chapter prices out in full.</p></div>

<p>Domino's ordering system sits at the expensive end: custom software, built and owned, because
Chapter 3 established that the ordering pipeline <em>is</em> the business, exactly the situation
where custom is worth it. Which makes the case sharper, not softer: this was not a neglected vendor
product the company barely controlled. It was the software Domino's chose to build itself, and the
gap in it was a gap in the company's own design decisions.</p>

<h2 id="s3"><span class="num">03</span>The interface decides who gets in</h2>

<p>For the first decades of computing, the interface was a command line: a blinking cursor awaiting
typed instructions in a syntax you had to already know. The population of people who could use a
computer was, in effect, the population willing to memorize it. The graphical interface, windows,
menus, a mouse, things you could recognize instead of recall, did not make computers more powerful.
It made them <em>usable by more people</em>, and the personal-computing industry is the direct
result. Hold that historical fact as a principle: every interface decision is a decision about who is
in your market.</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Usability</span>
<p><strong>Usability</strong> is not aesthetic preference; it is a set of measurable properties.
<strong>Learnability</strong>: how quickly can a new user do the core task? <strong>Efficiency</strong>:
how fast is the task once learned? <strong>Error tolerance</strong>: how easily do users make
mistakes, and how gracefully can they recover? You can put numbers on each, by watching real users
attempt real tasks, which is what Lab 9 will have you do. The business stakes compound quietly: a
confusing checkout leaks customers one abandoned cart at a time, and inside the company, hard-to-use
enterprise software taxes every employee every day, a cost that never appears on the invoice of the
system that causes it.</p></div>

<h2 id="s4"><span class="num">04</span>Accessibility is not a feature request</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Accessibility and WCAG</span>
<p><strong>Accessibility</strong> is usability's widest circle: designing software that works for
people with disabilities, including blind and low-vision users on screen readers, deaf users needing
captions, and people navigating by keyboard or voice because they cannot use a mouse. The World Wide
Web Consortium's <strong>Web Content Accessibility Guidelines (WCAG)</strong> are the de facto
standard, organized around four properties: content must be <em>perceivable</em>, <em>operable</em>,
<em>understandable</em>, and <em>robust</em>. In practice much of it is unglamorous discipline:
labeling images and buttons so a screen reader has something to say, making every function reachable
by keyboard, maintaining contrast a low-vision user can read.</p></div>

<p>Two facts reframe accessibility from charity to strategy. First, scale: the World Health
Organization estimates about one in six people worldwide live with a significant disability, a
market no retailer would knowingly lock out. Second, the <strong>curb-cut effect</strong>: features
built for disability keep turning out to serve everyone, the way sidewalk curb cuts built for
wheelchairs now serve strollers, suitcases, and delivery carts. Captions serve the noisy gym;
voice interfaces serve drivers; high contrast serves your phone in sunlight. Accessible design is,
reliably, just better design under constraints, and building it in from the start costs a fraction of
retrofitting it under a court deadline, which brings us back to the pizza.</p>

<h2 id="s5"><span class="num">05</span>The case: the ADA meets the web</h2>

<p>The district court initially sided with Domino's on procedure, reasoning that without federal
web-accessibility regulations, courts should wait for the Department of Justice to define the rules.
In January 2019 the Ninth Circuit Court of Appeals reversed, and its two holdings are the ones that
matter. First: Title III of the ADA applies to the websites and apps of a business where they connect
customers to the goods and services of its physical locations, the nexus that Domino's, with
thousands of stores, plainly had. The court put it directly: the website and app facilitate access to
the goods and services of a place of public accommodation. Second: the absence of formal regulations
is not a due-process escape hatch; the statute's obligation to communicate effectively with disabled
customers was itself fair notice. In October 2019 the Supreme Court declined to hear Domino's appeal,
leaving the ruling standing, and the case later ended in settlement.</p>

<p>Notice the structure of the legal lesson, because you have seen it before. In Chapter 8,
regulators' position on AI hiring tools was that existing discrimination law applies no matter how
novel the technology; here, a 1990 statute written before the web reached the web anyway, because
courts read laws by their purpose, not their era's technology. "There are no rules for this yet" is
one of the most expensive sentences in business, and the aftermath proved it: with the precedent
standing, web-accessibility suits, already climbing, now number in the thousands per year, and the
practical standard companies are held to is the WCAG guidance that was freely available the whole
time. The cheapest moment to meet it was before the lawsuit.</p>

<div class="pull"><p>The interface is a legal surface. Domino's learned it from a pizza order; every business with a website inherited the lesson.</p></div>

<h2 id="s6"><span class="num">06</span>How businesses choose software</h2>

<p>Design is one software decision; the other, far more common one is selection, because most
companies buy far more software than they build. Selection done badly is how organizations end up
with systems everyone hates, and Chapter 6 showed you the nine-figure version. The professional
process is unglamorous and learnable:</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Software selection and total cost of ownership</span>
<p>Start with <strong>requirements</strong>, written before any vendor demo, split into must-have
and nice-to-have, because a good demo will otherwise write your requirements for you. Shortlist, then
run <strong>scripted demos</strong>: every vendor performs <em>your</em> tasks on <em>your</em>
sample data, not their rehearsed happy path. Compute <strong>total cost of ownership (TCO)</strong>:
the license or subscription is often the minority of the real cost once implementation, integration,
training, support, and the eventual cost of leaving are added. Check references from companies your
size, then <strong>pilot</strong> with real users before committing. And after this chapter, one line
belongs in every requirements document: conformance with WCAG, verified in the demo with a screen
reader running, because Section 5 just established what that line is worth.</p></div>

<h2 id="s7"><span class="num">07</span>Build, buy, or subscribe</h2>

<p>The strategic layer of selection is the oldest question in corporate IT: build it, buy it, or
rent it? The working rule falls straight out of Chapter 2. If the capability is a
<strong>commodity</strong>, something every business does the same way, payroll, email, accounting,
buy or subscribe, because custom-building it buys you no advantage and all the maintenance. If the
capability is your <strong>differentiator</strong>, the thing customers choose you for, owning it can
be worth the enormous cost, which is why Domino's built its ordering pipeline and why Chapter 3's
whole story exists. The judgment call is knowing which is which, and the honest test is Porter's:
would doing this better than rivals actually change what customers do?</p>

<p>Hold this rule for Wednesday-to-Monday continuity: the next chapter's case is a company that
pushed it to the extreme, renting essentially all of its computing from its fiercest competitor
while spending heavily to build the one piece that touches the customer experience most. The rule
scales from a co-op's point-of-sale choice to a $100 billion streaming service without changing
shape.</p>

<h2 id="s8"><span class="num">08</span>The other side: who software forgets</h2>

<p>Robles is the visible case of a quiet, general pattern: software forgets the users its builders
did not picture. Disabled users are the sharpest example, but the circle is wider. Older users meet
interfaces tuned to reflexes trained by two decades of apps they never used. Low-income users meet
sites built and tested on new phones over fast connections. Non-native speakers meet error messages
written in idiom. None of this is malice; it is the default outcome of teams building for themselves,
which is why deliberate practices, accessibility standards, usability testing with people unlike the
builders, exist at all.</p>

<p>And one forgotten user lives inside the company: the employee. The person who selects enterprise
software is almost never the person who will use it eight hours a day, and the gap shows. The
warehouse worker fighting a fifteen-click process, the nurse clicking through screens designed by a
billing department, pay daily for a selection decision they were never consulted on. Section 6's
pilot step exists precisely to close that gap, and the best single question to ask about any software
purchase is the one this chapter has been circling: <em>who was in the room when this was chosen, and
who has to live with it?</em></p>

<h2 id="s9"><span class="num">09</span>The five components of the Robles case</h2>

<table class="sumtable">
<tr><th>Component</th><th>In the case</th><th>The lesson</th></tr>
<tr><td><strong>Hardware</strong></td><td>His phone and computer, standard equipment running assistive software</td><td>The barrier was never the device</td></tr>
<tr><td><strong>Software</strong></td><td>A custom-built site and app without the labels a screen reader needs</td><td>Design decisions are market decisions, and legal ones</td></tr>
<tr><td><strong>Data</strong></td><td>Menus, prices, and online-only coupons he could not reach</td><td>Information a customer cannot perceive may as well not exist</td></tr>
<tr><td><strong>Networks</strong></td><td>The web, which a 1990 statute reached anyway</td><td>New channels inherit old obligations</td></tr>
<tr><td><strong>People</strong></td><td>Builders who never tested with a screen reader; a customer who sued</td><td>The users you do not picture will find you eventually</td></tr>
</table>

<h2 id="s10"><span class="num">10</span>Summary and vocabulary</h2>

<table class="sumtable">
<tr><th>Idea</th><th>This chapter's version</th><th>Where you meet it next</th></tr>
<tr><td><strong>The interface as gatekeeper</strong></td><td>From command lines to Robles: design decides who is in the market</td><td>Lab 9's usability tests</td></tr>
<tr><td><strong>Accessibility</strong></td><td>One in six people, the curb-cut effect, and WCAG as the working standard</td><td>Your RFP's newest required line</td></tr>
<tr><td><strong>"No rules yet" is not "no obligation"</strong></td><td>A 1990 law reached the web; cert denied</td><td><a href="chapter8-ai-ml.html">Ch 8's AI governance</a>, same principle</td></tr>
<tr><td><strong>Selection discipline</strong></td><td>Requirements first, scripted demos, TCO, pilot</td><td>The Wednesday activity</td></tr>
<tr><td><strong>Build vs. buy vs. subscribe</strong></td><td>Own your differentiator, rent your commodities</td><td><a href="chapter12-cloud.html">Ch 12: Netflix takes it to the limit</a></td></tr>
</table>

<dl class="vocab">
<div><dt>System vs. application software</dt><dd>What runs the machine vs. what does the business's work.</dd></div>
<div><dt>Custom / packaged / SaaS</dt><dd>Built for you, bought off the shelf, or rented by subscription on the vendor's computers.</dd></div>
<div><dt>Usability</dt><dd>Measurable properties of an interface: learnability, efficiency, error tolerance.</dd></div>
<div><dt>Accessibility</dt><dd>Design that works for people with disabilities; usability's widest circle.</dd></div>
<div><dt>Screen reader</dt><dd>Assistive software that speaks an interface aloud, if the interface was built with the structure it needs.</dd></div>
<div><dt>WCAG</dt><dd>The Web Content Accessibility Guidelines: perceivable, operable, understandable, robust; the working legal standard.</dd></div>
<div><dt>Curb-cut effect</dt><dd>Features built for disability that end up serving everyone.</dd></div>
<div><dt>Public accommodation nexus</dt><dd>The Ninth Circuit's rule: the ADA reaches a site or app that connects customers to a physical business's goods and services.</dd></div>
<div><dt>Requirements / RFP</dt><dd>What the software must do, written down before any vendor demo can write it for you.</dd></div>
<div><dt>Scripted demo</dt><dd>Vendors performing your tasks on your data, not their rehearsed path.</dd></div>
<div><dt>Total cost of ownership</dt><dd>License plus implementation, integration, training, support, and the cost of leaving.</dd></div>
<div><dt>Build vs. buy vs. subscribe</dt><dd>Own your differentiator; rent your commodities.</dd></div>
</dl>

<div class="tps">
  <div class="tps-head"><span>Wednesday activity &middot; Pick a point-of-sale system for Cascadia</span><span class="mins">20 minutes</span></div>
  <div class="tps-body">
    <p class="tps-setup">The co-op's registers are aging out, and three finalists are on the table.
    <strong>SwiftRegister</strong> (SaaS): $79 per store per month, slick, running tomorrow, but its
    member-lookup screen fails basic screen-reader tests and it cannot talk to the membership
    database without a custom bridge. <strong>CoopSuite</strong> (packaged): $60,000 up front plus
    annual support, integrates natively with membership, WCAG-conformant, six-month implementation.
    <strong>OpenTill</strong> (open source): free license, fully flexible, accessible if configured
    correctly, but the co-op would own every problem and has no developer on staff.</p>
    <div class="tps-q"><p>Which do you recommend to the board? Commit before discussing, and name the requirement you are knowingly sacrificing.</p></div>
    <div class="tps-steps">
      <div class="tps-step"><div class="ph">Think <span>3 min</span></div><p>Choose, and write your sacrificed requirement honestly. "Nothing" is not available.</p></div>
      <div class="tps-step"><div class="ph">Pair <span>5 min</span></div><p>Find a different choice. Attack each other's pick with TCO first, then with the Robles test.</p></div>
      <div class="tps-step"><div class="ph">Share <span>12 min</span></div><p>We will build the comparison table on the board and watch the cheap option get expensive: the bridge, the retrofit, the lawsuit exposure, the staff time.</p></div>
    </div>
    <div class="tps-note"><strong>Where this lands</strong>There is a defensible case for two of the three, and the argument is the point: every software selection is a trade made explicit or a trade made by accident. The one indefensible move after this chapter is treating the accessibility failure as a footnote, because Section 5 priced that footnote. Sticker price is the smallest number in the decision.</div>
  </div>
</div>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach and sparring partner</strong>
  <p>Two good uses this week. Have an AI play the vendor: give it one of the activity's three systems
  and run a mock scripted demo, pressing it on integration and accessibility until it squirms. And
  draft your own requirements list first, then ask an AI what you missed; its additions will be
  generic, and deciding which generic requirements actually apply to a member co-op is exactly the
  selection judgment this chapter is teaching.</p></div>
</div>

<h2 id="questions"><span class="num">11</span>Discussion questions</h2>
<p><em>Groups of three; each group takes one and reports out.</em></p>
<ol class="dq">
<li>Domino's argued Robles could always order by phone. Steelman that argument, then explain why the Ninth Circuit's "full and equal enjoyment" framing defeats it. What would the phone-only rule imply for every other digital-first business?<span class="tag tag-open">Evaluate</span></li>
<li>The nexus rule covers sites connected to physical locations. Should the ADA reach web-only businesses with no storefront at all? Argue both sides, then say where you would draw the line and why.<span class="tag tag-hard">Judgment</span></li>
<li>Write the accessibility clause you would put in Cascadia's point-of-sale RFP: what must be true, how it will be verified in the demo, and what happens at contract time if the vendor falls short.<span class="tag tag-warm">Design</span></li>
<li>Give two curb-cut-effect examples from software you use daily: features that plausibly began as accessibility work and now serve you. What does the pattern suggest about how design constraints work?<span class="tag tag-open">Apply</span></li>
<li>Domino's chose to litigate for three years rather than remediate. Reconstruct that decision as its executives might have seen it in 2017, then judge it with hindsight. What did fighting actually buy, and what did it cost beyond legal fees?<span class="tag tag-hard">Judgment</span></li>
<li>Apply the build-buy-subscribe rule to three of Cascadia's needs: payroll, the member database, and the used-gear trade-in workflow from Lab 7's tables. Defend each placement.<span class="tag tag-warm">Apply</span></li>
<li>Section 8 argues the selector of enterprise software is rarely its daily user. Propose one governance mechanism, in the Chapter 10 sense, that would force selection decisions to answer to the people who live with them.<span class="tag tag-open">Connect</span></li>
<li>The GUI expanded who could use a computer; Section 3 called every interface decision a market decision. Name a group that current mainstream interfaces still exclude, and describe the interface change that would let them in.<span class="tag tag-hard">Design</span></li>
</ol>

<h2><span class="num">12</span>Sources and further reading</h2>
<ul class="sources">
<li><em>Robles v. Domino's Pizza LLC</em>, 913 F.3d 898 (9th Cir. 2019): the holdings that Title III of the ADA applies to a website and app with a nexus to physical locations, and that the absence of regulations raises no due-process bar.</li>
<li>Reporting on the Supreme Court's denial of certiorari, October 7, 2019 (ABA Journal and others): the ruling left standing, and the anticipated rise in web-accessibility litigation that followed.</li>
<li>W3C, Web Content Accessibility Guidelines (WCAG): the perceivable, operable, understandable, robust framework that functions as the practical compliance standard.</li>
<li>World Health Organization, World Report on Disability estimates: roughly one in six people worldwide live with significant disability, the market-scale figure in Section 4.</li>
<li>Coverage of the case's 2022 settlement (accessibility-industry reporting): the quiet ending, after the expensive route.</li>
</ul>

<p style="margin-top:2.5rem"><a href="schedule.html">Lab 9, UX Design, runs this week &#8594;</a></p>

''' + TAIL
open('chapter11-software.html','w').write(CH11)
print('chapter11-software.html:', len(CH11))

# ============================================================ CHAPTER 12
CH12 = make_head("Chapter 12: The Cloud &amp; What Computing Costs: Netflix",
 "Netflix's seven-year move onto its rival's computers, the CDN it built anyway, the day us-east-1 blinked, and the planet-sized bill behind every stream and prompt.")

CH12 += '''<main class="chapwrap">

<header class="chaphead">
  <p class="eyebrow">Chapter 12 &middot; Cloud &amp; What Computing Costs</p>
  <h1>The Cloud: Renting Computers, and the Bill the Planet Gets</h1>
  <p class="anchor">In August 2008 a database corruption stopped Netflix from shipping DVDs for three
  days, and the company drew a radical conclusion: stop owning computers. Seven years later it shut
  its last data center and ran one of the world's biggest services on machines rented from its
  fiercest competitor. This chapter is about what the cloud actually is, why renting won, what
  Netflix deliberately built anyway, what happens on the day the cloud blinks, and the question
  Chapter 8 left you holding: when computing feels free, who is paying, and in what currency?</p>
  <div class="meta-row">
    <span>Cases: Netflix / AWS &middot; IEA, Energy and AI</span>
    <span class="alt">Week 10 &middot; Wednesday, the final lecture</span>
    <span class="alt"><a href="schedule.html" style="color:inherit;text-decoration:none">Paired lab: Information Architecture (Lab 10) &#8594;</a></span>
  </div>
</header>

<div class="statrow">
  <div class="stat"><b>3 days</b><span>DVDs stopped; the decision that started it</span></div>
  <div class="stat"><b>7 yrs</b><span>to shut the last Netflix data center, 2016</span></div>
  <div class="stat"><b>130+</b><span>countries switched on in a single day</span></div>
  <div class="stat"><b>415 TWh</b><span>data centers' electricity in 2024, ~1.5% of the world's</span></div>
  <div class="stat"><b>&times;2</b><span>projected by 2030, roughly Japan's annual usage</span></div>
</div>

<div class="toc"><strong>Contents</strong>
<a href="#s1">1. Three days without DVDs</a>
<a href="#s2">2. What the cloud actually is</a>
<a href="#s3">3. Seven years to zero data centers</a>
<a href="#s4">4. The part Netflix built anyway</a>
<a href="#s5">5. When the cloud blinks</a>
<a href="#s6">6. The bill the planet gets</a>
<a href="#s7">7. What business people do with the cloud</a>
<a href="#s8">8. The other side: the cloud's neighbors</a>
<a href="#s9">9. The five components</a>
<a href="#s10">10. Summary and vocabulary</a>
<a href="#questions">11. Discussion questions</a>
</div>

<div class="plan">
<div class="plan-head">Wednesday session plan &middot; 80 minutes &middot; the last lecture of the quarter</div>
<table>
<tr><td class="t">0:00</td><td class="w">Open</td><td>Ask: where, physically, was the last thing you streamed? Collect guesses. Nobody knows, and by the end of the session everyone will, down to the box inside their internet provider.</td></tr>
<tr><td class="t">0:05</td><td class="w">Lecture</td><td>The Netflix arc: the 2008 corruption, IaaS/PaaS/SaaS and capex to opex, seven years to zero data centers, 130 countries in a day, and Open Connect as the build-versus-buy rule from Chapter 11 at its limit.</td></tr>
<tr><td class="t">0:35</td><td class="w">Lecture</td><td>The two bills: concentration risk, with the October 2025 us-east-1 morning as the fresh case, then the physical bill, walking the IEA numbers from 415 TWh to the doubling, the water, and who lives next to it.</td></tr>
<tr><td class="t">0:55</td><td class="w">Think-pair-share</td><td>Where does the co-op's data live? See the activity below.</td></tr>
<tr><td class="t">1:15</td><td class="w">Close</td><td>The course's last callback: trace one Spotify Wrapped play through all five components, from a phone through the pipeline to a rented GPU, and name each bill along the way. That trace is a fair preview of the final.</td></tr>
</table></div>

<h2 id="s1"><span class="num">01</span>Three days without DVDs</h2>

<p>By its own account, Netflix's road to the cloud began with a failure: in August 2008 a major
database corruption meant that for three days the company could not ship DVDs to its members. The
diagnosis went deeper than the incident. Netflix concluded it had to move away from vertically
scaled single points of failure, big databases in its own data center, toward horizontally scalable,
distributed systems it did not own, and it chose Amazon Web Services as the landlord. Pause on the
strangeness of that sentence: Amazon, whose Prime Video competes directly with Netflix, would
henceforth run the computers underneath Netflix. The logic was Chapter 11's rule pushed to its
limit: computing infrastructure had become a commodity Netflix could rent better than build, even
from a rival, freeing the company to spend its effort on what differentiates it.</p>

<h2 id="s2"><span class="num">02</span>What the cloud actually is</h2>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Cloud computing: IaaS, PaaS, SaaS, and capex to opex</span>
<p>Strip the vapor from the word: <strong>the cloud is other people's data centers, rented over the
network, usually by the hour</strong>. It comes in layers of pre-assembly.
<strong>Infrastructure as a service (IaaS)</strong> rents raw computing: virtual machines, storage,
networking, and you run everything above. <strong>Platform as a service (PaaS)</strong> rents a
higher floor: databases, queues, and tools the provider operates for you. <strong>Software as a
service (SaaS)</strong>, from Chapter 11, rents the finished application. Economically, the cloud
converts <strong>capital expenditure</strong>, buying servers years ahead of need, into
<strong>operating expenditure</strong>, paying for what you use as you use it. And technically it
delivers <strong>elasticity</strong>: capacity that expands in minutes and, just as importantly,
contracts, so nobody pays all year for the machines that only Thanksgiving weekend needs.</p></div>

<p>In five-components terms, the cloud is the hardware component becoming a utility, like power from
a grid instead of a generator in the basement. That framing also tells you what does not change:
renting the computers outsources none of the responsibility for the data on them, the software above
them, or the decisions about both, a point Chapter 9's third-party-risk lesson already made in
harder currency.</p>

<h2 id="s3"><span class="num">03</span>Seven years to zero data centers</h2>

<p>The migration took seven years, finishing in early January 2016 when Netflix shut down the last
data-center pieces serving its streaming product. The company is candid about why it took so long:
the easy path was to forklift existing systems into AWS unchanged, and Netflix refused it, because
that moves your problems along with your servers. Instead it rebuilt nearly everything cloud-native,
as distributed systems designed to expect failure. The payoff figures come from Netflix's own
announcement: eight times the streaming members it had in 2008, overall viewing up three orders of
magnitude, and elasticity that let engineers add thousands of virtual servers and petabytes of
storage in minutes. The proof-of-concept moment came the same month the migration ended: on January
6, 2016, Netflix switched on service in more than 130 additional countries at once, a launch its own
racks could never have absorbed.</p>

<p>One more habit came out of the rebuild, and it belongs in your vocabulary as culture, not
technology. Having been burned by a Christmas Eve 2012 outage in an AWS load-balancing service,
Netflix institutionalized the assumption that everything fails: it built tools, famously including
one called Chaos Monkey, that deliberately break pieces of its own production systems so engineers
are forced to design for the failure before it happens for real. Chapter 9 called the rehearsed plan
for the bad day business continuity. Netflix automated the rehearsal.</p>

<h2 id="s4"><span class="num">04</span>The part Netflix built anyway</h2>

<p>Here is the detail that turns the case from a cloud advertisement into a strategy lesson.
Everything that happens before you press Play, sign-in, search, recommendations, billing, runs on
AWS. The video itself does not. Netflix built and owns <strong>Open Connect</strong>, its private
<strong>content delivery network (CDN)</strong>: purpose-built appliances loaded with the catalog
and installed inside internet service providers around the world, so the actual stream travels a few
network hops from a Netflix-owned box near you, not across the planet from a rented one. Open
Connect carries the entirety of Netflix's video traffic, tens of terabits per second at peak, one of
the highest-volume networks in existence.</p>

<p>Run Chapter 11's rule over the split and it resolves perfectly. Elastic, spiky, commodity
computing: rent it, even from a rival. The predictable, colossal, quality-defining flow of bits that
<em>is</em> the customer experience: own it, tune it, and let it become a moat. The lesson is not
"use the cloud" or "avoid the cloud"; it is that build-versus-rent is decided capability by
capability, by the same differentiator test, at every scale from Cascadia's registers to a third of
the internet's evening traffic.</p>

<h2 id="s5"><span class="num">05</span>When the cloud blinks</h2>

<p>Concentration risk, Chapter 9's word for a third of US medical claims flowing through one
company, has a computing version, and it demonstrated itself recently. In October 2025 a failure in
AWS's largest region, US-East-1 in Northern Virginia, rooted in a DNS fault involving its DynamoDB
database service, cascaded for the better part of a day. Thousands of services stumbled at once:
social apps, games, banks, airlines, smart-home devices, companies whose customers had no idea AWS
existed until the morning it mattered. Nothing was hacked. One landlord had a bad day, and a
noticeable slice of the internet had it too.</p>

<div class="kc"><span class="kc-tag">Key concept</span><span class="kc-term">Lock-in, egress, and the cost of leaving</span>
<p>The strategic mirror of concentration risk is <strong>vendor lock-in</strong>. Cloud providers
price movement asymmetrically: data flows in free and pays <strong>egress fees</strong> on the way
out, and every provider-specific service your engineers adopt deepens the rebuild required to leave.
This is Chapter 2's <strong>switching costs</strong>, implemented in infrastructure. The remedies,
spreading across regions or across providers, are real and expensive, which makes resilience what it
has been all course: not a technical setting but a business decision about how much insurance to
buy, made before the morning it is needed.</p></div>

<h2 id="s6"><span class="num">06</span>The bill the planet gets</h2>

<p>Chapter 8 ended with a promissory note: when the For You page or a chatbot answer feels free, who
is paying, and in what currency? This section pays it, with the International Energy Agency's
ledger. In 2024, the world's data centers consumed roughly <strong>415 terawatt-hours</strong> of
electricity, about <strong>1.5 percent of all electricity on Earth</strong>, and the figure has grown
around 12 percent a year since 2017, four times faster than electricity use overall. The IEA's base
case projects consumption more than doubling to about <strong>945 TWh by 2030</strong>, roughly
Japan's entire current annual usage, with AI-accelerated servers driving close to half of the
increase. The United States hosts the largest share, around 45 percent, and data centers account for
nearly half of all US electricity-demand growth between now and 2030.</p>

<p>The global percentages stay small; the local ones do not, because the load clusters. Data centers
already consume on the order of a fifth of Ireland's electricity and, by commonly cited estimates, a
quarter of Virginia's, which is why siting fights, grid-upgrade bills, and moratorium debates now
follow the industry around. Electricity is also only the headline line item. Cooling the machines
consumes water, a sharpening issue where the cheap land and power happen to be dry. The accelerator
arms race turns over hardware fast enough to make e-waste a growing stream. And the electricity mix
matters as much as the amount: today it leans on coal and gas alongside renewables and nuclear,
putting data-center emissions in the hundreds of millions of tonnes of CO2 per year. None of this is
an argument that streaming a show is shameful; a single stream or prompt costs very little. It is an
argument that <em>at scale, computing is industry</em>, with industry's bills, and that the people
who plan, site, buy, and account for it, which is to say people with business degrees, decide how
those bills get paid.</p>

<h2 id="s7"><span class="num">07</span>What business people do with the cloud</h2>

<p><strong>Cloud cost management, now a discipline called FinOps.</strong> Elasticity cuts both
ways: capacity that scales up in minutes generates bills that do too, and someone must own the
question of what the company is paying for and why. Rightsizing, reservations, and the monthly
argument about whose workload that is: analytical work, sitting exactly on Lab 5's skills.</p>

<p><strong>Vendor strategy and negotiation.</strong> Section 5 made lock-in a business problem, so
contracts, egress terms, exit plans, and multi-cloud trade-offs are procurement strategy with
Chapter 2's switching-cost math at the center.</p>

<p><strong>Continuity planning.</strong> Deciding, before the next us-east-1 morning, which of the
company's systems must survive a provider region failing, and what that insurance is worth: Chapter
9's discipline, applied to the landlord.</p>

<p><strong>Sustainability accounting.</strong> Emissions from rented computing increasingly land in
corporate climate reporting, and regulators and customers are learning to read it. Someone has to
measure the footprint of systems the company does not own, negotiate greener regions and contracts,
and answer for the trend line: Chapter 7's measurement-validity problem, with a planet attached.</p>

<h2 id="s8"><span class="num">08</span>The other side: the cloud's neighbors</h2>

<p>The cloud's benefits disperse globally; its burdens concentrate locally, and the people carrying
them rarely chose to. A data-center cluster arrives with jobs and tax revenue, and also with demand
that can strain the local grid and, in some markets, shows up in residential electricity debates. In
dry regions, its cooling competes for water with farms and towns. Its diesel backup generators and
constant mechanical hum are a neighbor's daily reality, not an abstraction. Communities from
Northern Virginia to Ireland to the Southwest are now negotiating, and sometimes fighting, over
whether and how the next campus gets built.</p>

<p>You have seen this structure twice before: security costs exported to patients in Chapter 9, AI's
costs exported to applicants and labelers in Chapter 8. Economists call it an externality all three
times, and the governance answer is the same all three times: someone has to represent the people
who are not in the room when the decision is made. This course keeps returning to that sentence
because, in an economy that runs on information systems, the person in the room is increasingly
someone with your degree.</p>

<h2 id="s9"><span class="num">09</span>The five components of the cloud</h2>

<table class="sumtable">
<tr><th>Component</th><th>In the case</th><th>The lesson</th></tr>
<tr><td><strong>Hardware</strong></td><td>Rented by the hour from a rival; owned where the stream lives</td><td>Hardware became a utility, and the bill became strategy</td></tr>
<tr><td><strong>Software</strong></td><td>Rebuilt cloud-native; systems that assume their own failure</td><td>Moving unchanged moves your problems with you</td></tr>
<tr><td><strong>Data</strong></td><td>Everything before Play on AWS; the catalog staged inside ISPs</td><td>Data has gravity: where it sits decides cost, speed, and risk</td></tr>
<tr><td><strong>Networks</strong></td><td>Open Connect, tens of terabits per second of owned delivery</td><td>The network is not plumbing when it is the product</td></tr>
<tr><td><strong>People</strong></td><td>Engineers who break things on purpose; FinOps; the neighbors</td><td>Every rented machine still has humans deciding, and absorbing</td></tr>
</table>

<h2 id="s10"><span class="num">10</span>Summary and vocabulary</h2>

<table class="sumtable">
<tr><th>Idea</th><th>This chapter's version</th><th>Where you meet it next</th></tr>
<tr><td><strong>Capex to opex</strong></td><td>Rent computing as you use it; three days of stopped DVDs bought the insight</td><td>Every startup you will ever join</td></tr>
<tr><td><strong>Elasticity</strong></td><td>130 countries switched on in a day</td><td>The Wednesday activity's cost question</td></tr>
<tr><td><strong>Build vs. rent, per capability</strong></td><td>AWS underneath, Open Connect on top</td><td><a href="chapter11-software.html">Ch 11's rule</a>, at its limit</td></tr>
<tr><td><strong>Concentration risk</strong></td><td>One region's DNS fault, a slice of the internet's bad morning</td><td><a href="chapter9-changehealthcare.html">Ch 9's lesson</a>, in infrastructure</td></tr>
<tr><td><strong>The physical bill</strong></td><td>415 TWh, doubling; water, waste, and neighbors</td><td><a href="chapter8-ai-ml.html">Ch 8's question</a>, answered</td></tr>
</table>

<dl class="vocab">
<div><dt>Cloud computing</dt><dd>Other people's data centers, rented over the network, usually by the hour.</dd></div>
<div><dt>IaaS / PaaS / SaaS</dt><dd>Renting raw machines, a managed platform, or the finished application.</dd></div>
<div><dt>Capex vs. opex</dt><dd>Buying capacity years ahead versus paying for use as it happens.</dd></div>
<div><dt>Elasticity</dt><dd>Capacity that grows and shrinks in minutes, so peak demand stops dictating year-round cost.</dd></div>
<div><dt>Region / availability zone</dt><dd>The geographic units clouds are sold in; where your workload lives, fails, and is billed.</dd></div>
<div><dt>Content delivery network (CDN)</dt><dd>Servers placed near users so heavy content travels a short distance; Netflix's is Open Connect.</dd></div>
<div><dt>Chaos engineering</dt><dd>Breaking your own systems on purpose so failure is designed for before it is suffered.</dd></div>
<div><dt>Vendor lock-in / egress fees</dt><dd>Switching costs implemented in infrastructure: free to arrive, priced to leave.</dd></div>
<div><dt>Concentration risk</dt><dd>Chapter 9's word, computing edition: too much of the internet on one landlord's floor.</dd></div>
<div><dt>FinOps</dt><dd>The discipline of managing cloud spend; elasticity's bill, owned by someone.</dd></div>
<div><dt>Data gravity</dt><dd>Compute and services accumulate around where the data already sits, which is why the first region choice lasts.</dd></div>
<div><dt>Data-center externalities</dt><dd>Energy, water, noise, and grid strain landing on neighbors of the buildout.</dd></div>
</dl>

<div class="tps">
  <div class="tps-head"><span>Wednesday activity &middot; Where does the co-op's data live?</span><span class="mins">20 minutes</span></div>
  <div class="tps-body">
    <p class="tps-setup">Cascadia has outgrown the back-office server running its member database and
    point-of-sale backend. Three options: a major cloud provider's Oregon region (cheapest, most
    capable, and you now know what a bad region morning looks like); a small regional provider
    running on hydropower (greener and local, pricier, fewer services, less certain to exist in ten
    years); or buying new servers for the back office again (owned, patched by whom, exactly?). The
    co-op's members vote on values as well as budgets.</p>
    <div class="tps-q"><p>Which do you recommend, and what is the single fact from this quarter, a number, a case, a lab finding, that most drives your choice?</p></div>
    <div class="tps-steps">
      <div class="tps-step"><div class="ph">Think <span>3 min</span></div><p>Choose, and write your driving fact. It must be something you can cite, not a vibe.</p></div>
      <div class="tps-step"><div class="ph">Pair <span>5 min</span></div><p>Find a different choice. Stress-test each other with Week 8: whichever option you picked, who patches it, and what is the plan for its bad morning?</p></div>
      <div class="tps-step"><div class="ph">Share <span>12 min</span></div><p>We will map the answers to the quarter: TCO from Chapter 11, continuity from Chapter 9, the physical bill from today, and the co-op's values, which are a real constraint, not decoration.</p></div>
    </div>
    <div class="tps-note"><strong>Where this lands</strong>All three are defensible, which is the point of the last activity of the quarter: this is not a technology question with a right answer but a management question with trade-offs you can now name, price, and defend. That was the course.</div>
  </div>
</div>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach and sparring partner</strong>
  <p>Quiz yourself on the three service layers until you can place any product you use (your email,
  your bank's app, a game server) on the right one. Then one last audit in the Lab 1 spirit: ask an
  AI to estimate the energy cost of an hour of streaming, and check its confident number against the
  reasoning in Section 6. If the quarter worked, you will catch what needs catching.</p></div>
</div>

<h2 id="questions"><span class="num">11</span>Discussion questions</h2>
<p><em>Groups of three; each group takes one and reports out.</em></p>
<ol class="dq">
<li>Netflix rents its computing from a direct competitor. Run the five forces on that arrangement: what power does Amazon hold over Netflix, what limits that power, and why has the arrangement held for over a decade anyway?<span class="tag tag-open">Connect</span></li>
<li>State the build-versus-rent rule the Open Connect split implies, in one sentence. Then apply it to a hospital deciding where its patient-records system should run, and note what changes when Chapter 9's stakes enter the equation.<span class="tag tag-hard">Apply</span></li>
<li>Write Cascadia's one-page plan for the next us-east-1 morning: what must keep working in the stores, what can wait, and what the manual fallback is. Chapter 9 gave you the vocabulary; this asks for the artifact.<span class="tag tag-warm">Design</span></li>
<li>Make the strongest case that moving to the cloud is the greener choice for a typical company, then the strongest case that the cloud's growth is an environmental problem no individual migration decision addresses. Both are supportable; reconcile them.<span class="tag tag-hard">Judgment</span></li>
<li>Data centers are driving grid upgrades whose costs can reach ordinary ratepayers. Who should pay: the data-center customers, the tech companies, all ratepayers, or taxpayers? Argue your allocation and name its losers honestly.<span class="tag tag-hard">Judgment</span></li>
<li>Egress fees make data cheap to bring and expensive to remove. Using Chapter 2, explain why providers price it this way, and propose the contract clause you would demand before a migration if you were Cascadia's negotiator.<span class="tag tag-open">Connect</span></li>
<li>A friend says "I feel guilty streaming in HD now." Correct their model using Section 6: what is true, what is out of proportion, and where does individual behavior actually rank against siting, sourcing, and efficiency decisions?<span class="tag tag-open">Explain</span></li>
<li>The final synthesis: trace one Spotify Wrapped play from a phone tap to the narrative on screen, naming all five components at each hop and every bill along the way, financial and physical. This is the whole course in one trace, and a fair preview of the final exam.<span class="tag tag-hard">Synthesize</span></li>
</ol>

<h2><span class="num">12</span>Sources and further reading</h2>
<ul class="sources">
<li>Netflix Technology Blog / About Netflix, <a href="https://about.netflix.com/en/news/completing-the-netflix-cloud-migration">Completing the Netflix Cloud Migration</a> (February 2016): the 2008 database corruption, the seven-year timeline, the cloud-native rebuild, the growth figures, and the January 2016 global launch.</li>
<li>Netflix Open Connect documentation and industry coverage: the company-owned CDN carrying the entirety of Netflix's video traffic from appliances inside ISPs, at tens of terabits per second of peak.</li>
<li>International Energy Agency, <a href="https://www.iea.org/reports/energy-and-ai">Energy and AI</a> (2025): the 415 TWh / ~1.5% figure for 2024, the ~945 TWh 2030 base case, the growth rates, the US share, and the role of AI-accelerated servers.</li>
<li>Reporting on the October 2025 AWS US-East-1 outage (major outlets and AWS's own post-incident summary): the DNS fault involving DynamoDB and the day of cascading disruption across thousands of services.</li>
<li>Netflix Technology Blog on the Christmas Eve 2012 ELB outage and the Simian Army: the origin of chaos engineering as institutional habit.</li>
</ul>

<p style="margin-top:2.5rem"><a href="schedule.html">Lab 10, Information Architecture, closes the quarter &#8594;</a></p>

''' + TAIL
open('chapter12-cloud.html','w').write(CH12)
print('chapter12-cloud.html:', len(CH12))

# ============================================================ site-wide nav: add 11, 12; remove soon line
OLD_CH10 = '<a href="chapter10-equifax.html"><span class="lbl">Chapter 10 &middot; Week 8</span>IT Governance &mdash; Equifax</a>'
NEW_TAIL_NAV = OLD_CH10 + '''
      <a href="chapter11-software.html"><span class="lbl">Chapter 11 &middot; Week 9</span>Software Design &amp; Selection &mdash; Robles v. Domino's</a>
      <a href="chapter12-cloud.html"><span class="lbl">Chapter 12 &middot; Week 10</span>The Cloud &amp; What Computing Costs &mdash; Netflix</a>'''
SOON_BLOCK = '''
      <div class="dd-sep"></div>
      <a class="soon" href="#"><span class="lbl">Chapters 11&ndash;12</span>Cloud, IoT (in progress)</a>'''

for fn in glob.glob('*.html'):
    t = open(fn).read(); orig = t
    cur = OLD_CH10.replace('<a href', '<a class="current" href')
    if cur in t:
        t = t.replace(cur, NEW_TAIL_NAV.replace('<a href="chapter10-equifax.html">',
                                                '<a class="current" href="chapter10-equifax.html">'))
    else:
        t = t.replace(OLD_CH10, NEW_TAIL_NAV)
    t = t.replace(SOON_BLOCK, '')
    t = t.replace('<a href="%s">' % fn, '<a class="current" href="%s">' % fn)
    if t != orig:
        open(fn, 'w').write(t); print('nav:', fn)

# ============================================================ schedule + ch8 forward links
s = open('schedule.html').read()
s = s.replace('<h4 class="pending">Software: design and selection<span class="pill wip">Chapter in progress</span></h4>',
              '<h4><a href="chapter11-software.html">Software: design and selection</a></h4>')
s = s.replace('<h4 class="pending">Cloud, data centers, and what computing costs<span class="pill wip">Chapter in progress</span></h4>',
              '<h4><a href="chapter12-cloud.html">Cloud, data centers, and what computing costs</a></h4>')
open('schedule.html','w').write(s); print('schedule linked')

c = open('chapter8-ai-ml.html').read()
c = c.replace('<span class="alt"><a href="schedule.html" style="color:inherit;text-decoration:none">Wednesday: what computing costs &#8594;</a></span>',
              '<span class="alt"><a href="chapter12-cloud.html" style="color:inherit;text-decoration:none">Wednesday: what computing costs &#8594;</a></span>')
c = c.replace('<p style="margin-top:2.5rem"><a href="schedule.html">Wednesday: cloud, data centers, and what computing costs &#8594;</a></p>',
              '<p style="margin-top:2.5rem"><a href="chapter12-cloud.html">Wednesday: cloud, data centers, and what computing costs &#8594;</a></p>')
open('chapter8-ai-ml.html','w').write(c); print('chapter 8 forward links updated')
