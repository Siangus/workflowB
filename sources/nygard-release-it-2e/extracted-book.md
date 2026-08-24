# Release It!, Second Edition

- **book_id:** `nygard-release-it-2e`
- **source_epub:** `E:\下载\Release It! _ Design and Deploy Production-Ready Software -- Michael T_ Nygard -- 2nd edition, 2018 -- The Pragmatic Bookshelf -- isbn13 9781680502398 -- 1825a0ea05fa5b46605fa0c242046952 -- Anna’s Archive.epub`

## Source Map

## Chapter 1: Living in Production

<!-- source files: f_0010.xhtml -->

Release It! Second Edition
Chapter
 1
Living in Production
You’ve worked hard on your project. It looks like all the features are
 actually complete, and most even have tests. You can breathe a sigh of
 relief. You’re done.
Or are you?
Does “feature complete” mean “production ready”? Is your system really
 ready to be deployed? Can it be run by operations and face the hordes of
 real-world users without you? Are you starting to get that sinking feeling
 that you’ll be faced with late-night emergency phone calls and alerts? It
 turns out there’s a lot more to development than just adding all the
 features.
Software design as taught today is terribly incomplete. It only talks about
 what systems
should
do. It doesn’t address the converse—what
 systems should
not
do. They should not crash, hang, lose data,
 violate privacy, lose money, destroy your company, or kill your customers.
Too often, project teams aim to pass the quality assurance (QA) department’s tests instead of aiming for life
 in production. That is, the bulk of your work probably focuses on passing
 testing. But testing—even agile, pragmatic, automated testing—is not
 enough to prove that software is ready for the real world. The stresses and
 strains of the real world, with crazy real users, globe-spanning traffic,
 and virus-writing mobs from countries you’ve never even heard of go well
 beyond what you could ever hope to test for.
But first, you will need to accept the fact that despite your best laid
 plans, bad things will still happen. It’s always good to prevent them when
 possible, of course. But it can be downright fatal to assume that you’ve
 predicted and eliminated all possible bad events. Instead, you want to take
 action and prevent the ones you can but make sure that your system as a whole
 can recover from whatever unanticipated, severe traumas might befall it.

## Chapter 2: Case Study: The Exception That Grounded an Airline

<!-- source files: f_0018.xhtml -->

Release It! Second Edition
Chapter
 2
Case Study: The Exception That Grounded an Airline
Have you ever noticed that the incidents that blow up into the biggest issues
 start with something very small? A tiny programming error starts the snowball
 rolling downhill. As it gains momentum, the scale of the problem keeps
 getting bigger and bigger. A major airline experienced just such an incident.
 It eventually stranded thousands of passengers and cost the company hundreds
 of thousands of dollars. Here’s how it happened.
As always, all names, places, and dates have been changed to protect the
 confidentiality of the people and companies involved.
It started with a planned failover on the database cluster that served the
 core facilities (
CF
). The airline was moving toward a
 service-oriented architecture, with the usual goals of increasing reuse,
 decreasing development time, and decreasing operational costs. At this time,
 CF was in its first generation. The CF team planned a phased rollout, driven
 by features. It was a sound plan, and it probably sounds familiar—most
 large companies have some variation of this project underway now.
CF handled flight searches—a common service for any airline
 application. Given a date, time, city, airport code, flight number, or any
 combination thereof, CF could find and return a list of flight details. When this
 incident happened, the self-service check-in kiosks, phone menus, and
 “channel partner” applications had been updated to use CF. Channel partner
 applications generate data feeds for big travel-booking sites. IVR and
 self-service check-in are both used to put passengers on airplanes—“butts
 in seats,” in the vernacular. The development schedule had plans for new
 releases of the gate agent and call center applications to transition to CF
 for flight lookup, but those had not been rolled out yet. This turned out to
 be a good thing, as you’ll soon see.
The architects of CF were well aware of how critical it would be to the business. They built
 it for high availability. It ran on a cluster of J2EE application servers
 with a redundant Oracle 9i database. All the data were stored on a large
 external RAID array with twice-daily, off-site backups on tape and on-disk
 replicas in a second chassis that were guaranteed to be five minutes
 old at most. Everything was on real hardware, no virtualization. Just melted sand,
 spinning rust, and the operating systems.
The Oracle database server ran on one node of the cluster at a time,
 with Veritas Cluster Server controlling the database server, assigning the
 virtual IP address, and mounting or unmounting filesystems from the RAID
 array. Up front, a pair of redundant hardware load balancers directed
 incoming traffic to one of the application servers. Client applications like
 the server for check-in kiosks and the IVR system would connect to the
 front-end virtual IP address. So far, so good.
The
diagram
probably looks familiar. It’s a common
 high-availability architecture for physical infrastructure, and it’s a good
 one. CF did not suffer from any of the usual single-point-of-failure
 problems. Every piece of hardware was redundant: CPUs, drives, network cards,
 power supplies, network switches, even down to the fans. The servers were
 even split into different racks in case a single rack got damaged or
 destroyed. In fact, a second location thirty miles away was ready to take
 over in the event of a fire, flood, bomb, or attack by Godzilla.

## Chapter 3: Stabilize Your System

<!-- source files: f_0026.xhtml -->

Release It! Second Edition
Chapter
 3
Stabilize Your System
New software emerges like a new college graduate: full of optimistic
 vigor, suddenly facing the harsh realities of the world outside the
 lab. Things happen in the real world that just do not happen in the
 lab—usually bad things. In the lab, all the tests are contrived by
 people who know what answer they expect to get. The challenges your software
 encounters in the real world don’t have such neat answers.
Enterprise software must be cynical. Cynical software expects bad things to
 happen and is never surprised when they do. Cynical software doesn’t
 even trust itself, so it puts up internal barriers to protect itself
 from failures. It refuses to get too intimate with other systems,
 because it could get hurt.
The airline’s Core Facilities project discussed in Chapter 2,
​
Case Study: The Exception That Grounded an Airline
​
, was
 not cynical enough. As so often happens, the team got caught up in the
 excitement of new technology and advanced architecture. It had lots of great
 things to say about leverage and synergy. Dazzled by the dollar signs, it
 didn’t see the stop sign and took a turn for the worse.
Poor stability carries significant real costs. The obvious cost is lost
 revenue. The retailer from Chapter 1,
​
Living in Production
​
, loses
 $1,000,000 per hour of downtime, and that’s during the off-season. Trading
 systems can lose that much in a single missed transaction!
Industry studies show that it costs up to $150 for an online
 retailer to acquire a customer. With 5,000 unique visitors per hour, assume
 10 percent of those would-be visitors walk away for good. That’s $75,000
 in wasted marketing.
[2]
Less tangible, but just as painful, is lost reputation. Tarnish to the brand
 might be less immediately obvious than lost customers, but try having your
 holiday-season operational problems reported in
Bloomberg Businessweek
.
 Millions of dollars in image advertising—touting online customer
 service—can be undone in a few hours by a batch of bad hard drives.
Good stability does not necessarily cost a lot. When building the
 architecture, design, and even low-level implementation of a system, many decision points
 have high leverage over the system’s ultimate
 stability. Confronted with these leverage points, two paths might both
 satisfy the functional requirements (aiming for QA). One will lead to hours
 of downtime every year, while the other will not. The amazing thing is that
 the highly stable design usually costs the same to implement as the unstable
 one.

## Chapter 4: Stability Antipatterns

<!-- source files: f_0033.xhtml -->

Release It! Second Edition
Chapter
 4
Stability Antipatterns
Delegates to the first NATO Software Engineering Conference coined the term
software crisis
in 1968. They meant that demand for new software
 outstripped the capacity of all existing programmers worldwide. If that
 truly was the start of the software crisis, then it has never ended!
 (Interestingly, that conference also appears to be the origin of the term
software engineering
. Some reports say it was named that way so
 certain attendees would be able to get their travel expenses approved. I
 guess that problem hasn’t changed much either.) Our machines have gotten better by
 orders of magnitude. So have the languages and libraries. The enormous
 leverage of open source multiplies our abilities. And of course,
 something like a million times more programmers are in the world now than there were in
 1968. So overall, our ability to create software has had its own kind of
 Moore’s law exponential curve at work. So why are we still in a software
 crisis? Because we’ve steadily taken on bigger and bigger challenges.
In those hazy days of the client/server system, we used to think of a
 hundred active users as a large system; now we think about millions. (And
 that’s up from the first edition of this book, when ten thousand active users
 was a lot.) We’ve just seen our first billion-user site. In 2016, Facebook
 announced that it has 1.13
billion
daily active
 users.
[3]
An “application” now consists of dozens or hundreds of services, each
 running continuously while being redeployed continuously. Five nines of
 reliability for the overall application is nowhere near enough. It would
 result in thousands of disappointed users every day. Six Sigma quality on
 Facebook would create 768,000 angry users per day. (200 requests per page,
 1.13 billion daily active users, 3.4 defects per million opportunities.)
The breadth of our applications’ reach has exploded, too. Everything within the
 enterprise is interconnected, and then again as we integrate across
 enterprises. Even the boundaries of our applications have become fuzzy as
 more features are delegated to SaaS services.
Of course, this also means bigger challenges. As we integrate the world,
 tightly coupled systems are the rule rather than the exception. Big systems
 serve more users by commanding more resources; but in many failure modes
 big systems fail faster than small systems. The size and the complexity of
 these systems push us to what author James R. Chiles calls in
Inviting Disaster
[Chi01]
the
 “technology frontier,” where the twin specters of high interactive
 complexity and tight coupling conspire to turn rapidly moving cracks into
 full-blown failures.
High interactive complexity arises when systems have enough moving parts and
 hidden, internal dependencies that most operators’ mental models are either
 incomplete or just plain wrong. In a system exhibiting high interactive
 complexity, the operator’s instinctive actions will have results ranging from
 ineffective to actively harmful. With the best of intentions, the operator
 can take an action based on his or her own mental model of how the system
 functions that triggers a completely unexpected linkage. Such linkages
 contribute to “problem inflation,” turning a minor fault into a
 major failure. For example, hidden linkages in cooling monitoring and control
 systems are partly to blame for the Three Mile Island reactor incident, as
 Chiles outlines in his book. These hidden linkages often appear obvious during the
 postmortem analysis, but are in fact devilishly difficult to anticipate.
Tight coupling allows cracks in one part of the system to propagate
 themselves—or multiply themselves—across layer or system boundaries. A
 failure in one component causes load to be redistributed to its peers and
 introduces delays and stress to its callers. This increased stress makes it
 extremely likely that another component in the system will fail. That in turn
 makes the next failure more likely, eventually resulting in total
 collapse. In your systems, tight coupling can appear within application code,
 in calls between systems, or any place a resource has multiple consumers.
In the next chapter, we’ll look at some patterns that can alleviate or
 prevent the antipatterns from harming your system. Before we can get to that
 good news, though, we need to understand what we’re up against.
In this chapter, we’ll look at antipatterns that can wreck your system.
 These are common forces that have contributed to more than one system
 failure. Each of these antipatterns will create, accelerate, or multiply
 cracks in the system. These bad behaviors are to be avoided.
Simply avoiding these antipatterns isn’t sufficient, though. Everything
 breaks. Faults are unavoidable. Don’t pretend you can eliminate every
 possible source of them, because either nature or nurture will create bigger
 disasters to wreck your systems. Assume the worst. Faults will happen. We
 need to examine what happens
after
the fault creeps in.

## Chapter 5: Stability Patterns

<!-- source files: f_0047.xhtml -->

Release It! Second Edition
Chapter
 5
Stability Patterns
We have traveled through the vale of shadows. Now it is time to come in to
 the light. In the last chapter, we saw the antipatterns to avoid. In this chapter,
 we’ll look at the flip side and examine some patterns that are the inverse of
 the killers from the last chapter. These healthy patterns provide the
 architecture and design guidance to reduce, eliminate, or mitigate the
 effects of cracks in the system. Not one of these will help your software
 pass QA, but they
will
help you get a full night’s sleep, or at least an
 uninterrupted dinner with your family, once your software launches.
Don’t make the mistake of assuming that a system that includes more of these
 patterns is superior to one with fewer of them. “Count of patterns applied”
 is never a good quality metric. Instead, I want you to develop a
 recovery-oriented mind-set. At the risk of sounding like a broken record,
 I’ll say it again: expect failures. Apply these patterns wisely to reduce
 the damage done by an individual failure.

## Chapter 6: Case Study: Phenomenal Cosmic Powers, Itty-Bitty Living Space

<!-- source files: f_0063.xhtml -->

Release It! Second Edition
Chapter
 6
Case Study: Phenomenal Cosmic Powers, Itty-Bitty Living Space
In the middle 1500s, a Calabrian doctor named Aloysius Lilius invented a
 new calendar to fix a bug in the widely used Julian calendar. The Julian
 calendar had an accumulating drift. After a few hundred years, the official
 calendar date for the solstice would occur weeks before the actual
 event. Lilius’s calendar used an elaborate system of corrections and
 countercorrections to keep the official calendar dates for the equinoxes
 and solstices close to the astronomical events. Over a 400-year cycle, the
 calendar dates vary by as much as 2.25 days, but they vary predictably and
 periodically; overall, the error is cyclic, not cumulative. This calendar,
 decreed by Pope Gregory XIII, became known as the Gregorian calendar rather
 than the Lilian calendar. (They just use your mind and they never give you
 credit. It’s enough to drive you crazy if you let it.) The Gregorian
 calendar was eventually adopted by all European nations, although not
 without struggles, and even by Egypt, China, Korea, and Japan (with
 modifications for the latter three). Some nations adopted this calendar as
 early as 1582, while others adopted it only in the 1920s.
It’s no wonder that the church decreed the calendar. The Gregorian
 calendar, like most calendars, was created to mark holy days (that is,
 holidays). It has since been used to mark useful recurring events in
 certain other domains that depend on the annual solar cycle, such as
 agriculture. No business in the world actually lives by the Gregorian
 calendar, though. The business community uses the dates as a convenient
 marker for its own internal business cycle.
Each industry has its own internal almanac. For a health insurance company, the
 year is structured around “open enrollment.” All plans take their
 bearings from the open enrollment period. Florists’ thinking is dominated
 by Valentine’s Day and Mother’s Day. Upstream from them, Colombian flower
 growers center their agricultural year to produce the blossoms for those
 florists. These landmarks happen to be marked with specific dates on the
 Gregorian calendar, but in the minds of florists and their entire extended
 supply chain, those seasons have their own significance beyond
 the official calendar date.
For retailers, the year begins and ends with the euphemistically named
 “holiday season.” Here we see a correspondence between various religious
 calendars and the retail calendar. Christmas, Hanukkah, and Kwanzaa all
 occur relatively close together. Since “Christmahannukwanzaakah” turns
 out to be difficult to say in meetings with a straight face, they call it the
 “holiday season” instead. Don’t be fooled, though. Retailers’ interest
 in the holiday season is strictly ecumenical—some might even call it
 cynical. Up to 50 percent of a retailer’s entire annual revenue occurs between
 November 1 and December 31.
In the United States, Thanksgiving—the fourth Thursday in November—is
 the de facto start of the retail holiday season. By long tradition, this is
 when consumers start getting serious about gift shopping, because there are
 usually a little less than 30 days left in the season at that point. Apparently,
 motivation by deadline crosses religious boundaries. Shopper panic sets in,
 resulting in a collective phenomenon known as Black Friday. Retailers
 encourage and reinforce this by changing their assortment, increasing
 stocks in stores, and advertising wondrous things. Traffic in physical
 stores can quadruple overnight. Traffic at online stores can increase by
 1,000 percent. This is the real load test, the only one that matters.

## Chapter 7: Foundations

<!-- source files: f_0074.xhtml -->

Release It! Second Edition
Chapter
 7
Foundations
In the last chapter, the operations team, my client, and I narrowly avoided a
 financial disaster. It was a difficult situation, and the “solution” was not
 exactly ideal. All of us would have been happier if it’d never happened. My
 team couldn’t fix the underlying problem—the delivery scheduling servers
 were outside our control. But I was able to diagnose the problem, and the
 operations center partially mitigated its effects. That was only possible
 because we already had good visibility into the running system. There
 certainly wasn’t time to add a bunch of logging calls inside the
 application. With runtime visibility, though, new logging wasn’t
 necessary. The applications revealed their problems. To apply the solution,
 we exercised control over the running system. There’s no way we could have
 recovered if we’d had to reboot the servers after every configuration change.
The next few chapters cover those key ingredients, leading us to
 a concept of “design for production.” Design for production means
 thinking about production issues as first-class concerns. That includes the
 production network, which might be considerably different from your development
 environment. It also includes logging and monitoring, runtime control, and
 security. Design for production also means designing for the people who do
 operations, whether they are a dedicated ops team or integrated with
 development. Operators are users, too. They may not be logged in to a
 beautifully designed front-end application, but they get to interact with
 your system through its configuration, control, and monitoring interfaces. If
 your system’s front end is Disney World, then operators get to use the secret
 tunnels beneath the park.
In the next several chapters, we will work through layers of concerns. As you
 can see in
the figure
, everything starts
 with the physical infrastructure. We’ll discuss that in this chapter. The
 next chapters each zoom out one step at a time to encompass wider, more
 distributed concerns as we go.
You may notice that the words “as a service” don’t appear anywhere in the
 diagram above. The distinctions between “Infrastructure as a Service” and
 “Platform as a Service” were never strong to begin with. As vendors have
 sliced, diced, and triangulated their way across the landscape, those
 classifications have broken down completely. It’s more useful to look at
 different technology platforms in terms of those layers of responsibility:
 Which layers do they drive/does the platform drive completely by API? Which
 responsibilities move from operations to developers, and in which
 layers? What
 responsibilities remain application-level concerns and what is moved behind
 software-driven abstractions?
This chapter starts with the first layer. Operations leads us into design for
 production considerations by looking at the physical fundamentals of the
 system: the machines and wires that everything else builds upon. The first
 order of business is to clear up some things about networks, hostnames, and
 IP addresses. After that, it’s time to talk about the code holders: physical
 hosts, virtual machines, and containers. Each kind of deployment has its own
 set of concerns that software designs must account for. Finally, we’ll look
 at some special concerns that arise when a system spans multiple data
 centers.

## Chapter 8: Processes on Machines

<!-- source files: f_0078.xhtml -->

Release It! Second Edition
Chapter
 8
Processes on Machines
In the last chapter, we looked at a diverse set of network and physical
 environments that our software may be deployed into. In this chapter, we’re
 going to focus on the individual instances. They need to be good citizens by
 providing transparency, accepting control, handling configuration nicely, and
 managing connections. We’ll see some natural overlap with the stability
 patterns from Chapter 5,
​
Stability Patterns
​
, since it’s the job of each
 instance to accept stress and insults with tolerance and grace.
In the car business, they say the engine needs fuel, fire, and air to
 work. Our version of that is code, config, and connection. Every machine
 needs the right code, configuration, and network connections. One problem
 we’re going to run into is that our vocabulary hasn’t really kept up with our
 technology. For instance, when some people say “server” they might mean a
 virtual machine running on a physical host in their data center. Others
 might mean a process inside an operating system, rather than a whole
 machine image. Technology like containers blur the lines further. A process
 in a container is also a process on the operating system that hosts the
 container. Which one should we call the “server?” At the risk of seeming
 hopelessly pedantic, we’ll try to agree on some terms that may help
 disambiguate the rest of this section.
Service
A collection of processes across machines that work together to deliver a
 unit of functionality. A service may have processes from multiple
 executables (for example, application code plus a database). One service
 may present a single IP address with load balancing behind the
 scenes. (More on that in Chapter 9,
​
Interconnect
​
.) On the other hand, it
 may have multiple IP addresses using the same DNS name.
Instance
An installation on a single machine (container, virtual, or physical) out
 of a load-balanced array of the same executable. A service can be made of
 multiple different types of executables, but when we talk about instances
 we refer to processes of the same executable, just running in multiple
 locations.
Executable
An artifact that a machine can launch as a process and created by a build
 process. In a compiled language, this will be a binary, whereas an
 interpreted language will include sources. For simplicity, “executable”
 also covers shared libraries that need to be installed before execution.
Process
An operating system process running on a machine; the runtime image of an
 executable.
Installation
The executable and any attendant directories, configuration files, and
 other resources as they exist on a machine.
Deployment
The act of creating an installation on a machine. Should be automated,
 with the deployment definition kept in source control.
To make this more concrete, take a look at the “Loan Request” service shown
 in the following deployment illustration.
In the deployment view, we’re concerned about
 transforming sources into binaries and binaries into deployments. This
 involves moving files around. The build process compiles the source code into
 binary executables that go into the package repository. As a build progresses
 through the deployment pipeline, various stages tag the build as having
 passed. If the build makes it all the way through the pipeline, the very same
 tagged binary gets laid down as an installation on each machine. All these files are inert during
 deployment. Now let’s look at the runtime view, shown in the
figure
.
In the runtime view, we’re more concerned with the processes running on the
 machines. (By the way, a lot of architectural confusion stems from attempts
 to cram both static and dynamic views into the same figure.) Each
 machine runs an instance of the same binary: our compiled service. Those
 instances all sit behind an HAProxy load balancer with the address
 10.10.128.19 bound to the DNS name loanrequest.example.com.
These definitions may seem persnickety, but teams have been bitten when
 different people use the same word for different things. Precise
 communication is especially important when dealing with operations. If you tell
 someone to “reboot the server,” you might not know which server they’re
 about to bounce, and you can’t be sure whether they’re going to kill a single
 process or the whole
 machine.
[21]
Now we can turn our attention to the code, config, and connection the
 instances require.

## Chapter 9: Interconnect

<!-- source files: f_0083.xhtml -->

Release It! Second Edition
Chapter
 9
Interconnect
In the previous chapter, we looked at instances running on machines. But really,
 who is interested in a single instance running by itself? A standalone
 process might as well be on a desert island. We need to connect them together
 into a system. This chapter continues our iterative zoom-out to look at how
 the instances work together and find each other, as well as how callers invoke them.
 It’s time to look at the “interconnect” layer from our schematic (shown
 in the following figure).
The interconnect layer covers all the mechanisms that knit a bunch of
 instances together into a cohesive system. That includes traffic management,
 load balancing, and discovery. The interconnect layer is where we can really
 create high availability. As with the instance level, we also need to create
 transparency and control. None of it happens by accident.

## Chapter 10: Control Plane

<!-- source files: f_0092.xhtml -->

Release It! Second Edition
Chapter
 10
Control Plane
In the preceding chapters we worked our way up from bare metal through
 layers of abstraction and virtualization to create a sea of instances running
 on machines. We’ve got software scattered around like an upended box of
 LEGO blocks. It’s up to the “control plane” to put these pieces in the right place
 and knit them together into a somewhat coherent whole.
The control plane encompasses all the software and services that run in the
 background to make production load successful. One way to think about it is
 this: if production user data passes through it, it’s production
 software. If its main job is to manage other software, it’s the control
 plane.
A challenge we’ll face in this chapter is that the solution space is not
 well partitioned among tools, packages, and vendors. It’s nowhere near as
 simple as picking one download from each column. There are overlaps and
 gaps. Not every combination will work together. No single package does
 everything. We are left with a lot of integration effort and plenty of
 trial and error.

## Chapter 11: Security

<!-- source files: f_0104.xhtml -->

Release It! Second Edition
Chapter
 11
Security
Poor security practices can damage your organization and many
 others. Your company may suffer direct losses from fraud or extortion. That
 damage gets multiplied by the cost of remediation, customer compensation,
 regulatory fines, and lost reputation. Individuals will lose their jobs, up
 to and including the
 CEO.
[50]
In 2017, the “WannaCry” ransomware affected more than 70 countries. It hit
 office computers, subway displays, and hospitals. The UK’s National Health
 Service got hit particularly hard, causing X-ray sessions to be canceled,
 stroke centers to close, and surgeries to be postponed. It put lives at risk.
[51]
In an epic game of one-upmanship, Equifax revealed in 2017 that 145.5
 million US consumers’ identities had been stolen.
[52]
And Yahoo! upped the ante in the same year when they announced that 3 billion
 Yahoo! accounts were stolen. We may have to discover alien life to get another
 order of magnitude increase.
System breaches aren’t always about extracting data. Sometimes they are about
 implanting it, as in the case of false identities or shipping documents. That
 kind of effort may have contributed to California’s nut theft crisis in
 2013.
[53]
Security must be baked in. It’s not a seasoning to sprinkle onto your system
 at the end. Even if your company has a dedicated security team, you aren’t
 off the hook. You’re still responsible to protect your customers and your
 company.
In this chapter, we’ll look at the “top ten” list of application
 vulnerabilities, as identified by the Open Web Application Security Project
 (OWASP). We’ll also consider data protection and integrity so that nobody loses
 their valuable nuts.

## Chapter 12: Case Study: Waiting for Godot

<!-- source files: f_0112.xhtml -->

Release It! Second Edition
Chapter
 12
Case Study: Waiting for Godot
It isn’t enough to write the code. Nothing is done until it runs in
 production. Sometimes the path to production is a smooth and open
 highway. Other times, especially with older systems, it’s a muddy track
 festooned with potholes, bandits, and checkpoints with border guards. This
 was one of the bad ones.
I turn my grainy eyes toward the clock on the wall. The hands point to 1:17
 a.m. I’d swear time has stopped. It has
 always been 1:17. I’ve seen enough film noir that I expect a fly to crawl
 across the face of the clock. There is no fly. Even the flies are asleep
 now. On the Polycom, someone is reporting status. It’s a DBA. One of the SQL
 scripts didn’t work right, but he “fixed” it by running it under a different
 user ID.
The wall clock doesn’t mean much right now. Our Lamport clock is still stuck
 a little before midnight. The playbook has a row that says SQL scripts finish
 at 11:50 p.m. We’re still on the SQL scripts, so logically we’re still at 11:50
 p.m. Before dawn, we need our playbook time and solar time to converge in
 order for this deployment to succeed.
The first row in the playbook started yesterday afternoon with a round of
 status reports from each area: dev, QA, content, merchants, order management,
 and so on. Somewhere on the first page of the playbook we had a go/no-go
 meeting at 3 p.m. Everyone gave the deployment a go, although QA said that
 they hadn’t finished testing and might still find a showstopper. After the
 go/no-go meeting, an email went out to the business stakeholders, announcing
 that the deployment would go forward. That email is their cue to go home, eat
 dinner at four in the afternoon, and get some sleep. We need them to get up at
 1 a.m. to “smoke test” the new features. That’s our UAT window: 1 to 3 a.m.
It’s 1:17 and the business stakeholders are awake and waiting to do their
 thing. I’m waiting to do my thing. When we get to about 12:40 in the playbook
 I run a script. I don’t know how long I’ll have to wait, but somehow I’m
 sure the clock will still say 1:17. Until then, I watch some numbers on a
 graph. In a release a couple of years ago, those numbers went the wrong
 way. So now we watch them. I know the code that triggered the problem was
 rewritten long ago. Nothing to be done. But the playbook calls for us to
 monitor those numbers and so we do. The release commander will sometimes ask
 what those numbers are.
Two days ago, we started reviewing and updating the playbook. We have a
 process for updating the process. The release commander walks through the
 whole thing row by row, and we confirm each row or update them for this
 particular release. Sometimes there are more steps, sometimes
 fewer. Different releases affect different features, so we need different
 people available to debug. Each review meeting takes two or three hours.
Around the long conference table, more than twenty heads are bowed over their
 laptops. They look like they are praying to the Polycoms: “Please say it
 worked. Please say it worked.” An equal number of people are dialed in to the
 same conference bridge from four locations around the world. In total, this
 release will consume more than forty of us over a 24-hour period. Most of the
 operations team members are here. The remainder are asleep so that they can be fresh to fix
 leftover problems in the morning. A while back we had an operator error that we blamed on
 fatigue. So now there’s a step in the playbook for the “B team”
 to go home and sleep. I tried to sneak in rows from Sandra Boynton’s
Going
 to Bed Book
—
“The day is done, they say goodnight.
And somebody turns off the light.”
But the playbook has no room for whimsy.
Our Lamport clock jumps forward while I’m not looking. The release
 commander tells Sys Ops to update symlinks. That’s my cue: I am Sys Ops. It’s
 not as cool as saying, “I am Iron Man.” The term “DevOps” won’t exist for
 another year, and in a different galaxy than this conference room. I tap
 Enter in my PuTTY window logged in to the jumphost—the only machine the
 others will accept SSH connections from. My script does three things on each
 machine. It updates a symbolic link to point to the new code drop, runs the
 JSP precompiler, and starts the server processes. A different script placed
 the code on the servers hours ago.
Now my turn is done until we finish UAT. Some energy gets generated when a
 voice emanates from the Polycom, informing us, “It didn’t work.” That
 may be the least helpful bug report ever received. It turns out the person
 was testing a page that wasn’t part of this release and had a known bug from
 two or three years back.
I don’t deal with boredom very well. After some fruitful contemplation on the
 nature of the buzz produced by fluorescent lights (and that the pitch must be
 different in countries on 50 hertz power), I start to wonder how much this
 deployment costs. A little napkin math surprises me enough that I make a
 spreadsheet. The size of the army times one day. I don’t know the cost
 structure, but I can guess that $100 per hour per person is not too far
 off. Add in some lost sales while the site is “gone fishing,” but not a lot
 because we’re offline during a slow part of the day. It’s about $100,000 to
 run this deployment. We do this four to six times a year.
Years later, I would witness a deployment at the online retailer Etsy. An
 investor was visiting, and as a routine part of the visit the company had him push
 the button to run its “deployinator.” The investor seemed pleased but not
 impressed. I felt a kind of bubbling hysteria. I needed to grab him by the
 collar. Didn’t he understand what that meant? How amazing it was? At the same
 time, I had a deep sense of loss: all that time in the deployment
 army. All that wasted potential. The wasted humanity! Using people as if they
 were bots. Disrupting lives, families, sleep patterns...it was all such a
 waste.
In the end, our deployment failed UAT. Some feature had passed QA because
 the data in the QA environment didn’t match production. (Stop me if you’ve heard
 this one before.) Production had extra content that included some JavaScript
 to rewrite part of a page from a third party and it didn’t work with the new
 page structure. The clock on the wall claimed it was around 5 a.m. when we
 finished the rollback procedure. That afternoon, we started planning the
 second attempt scheduled for two days hence.
You may have a deployment army of your own. The longer your production
 software has existed the more likely it is. In the following chapters, we’ll
 look at the forces that lead to this antipattern. We’ll also see how to
 climb out of the pit of despair. As you’ll see,
 making deployments faster and more routine has an immediate financial benefit. More than
 that, though, a virtuous cycle kicks in that gives you new superpowers. Best
 of all, you can stop wasting human potential on jobs that should be
 scripts.
Copyright © 2018, The Pragmatic Bookshelf.

## Chapter 13: Design for Deployment

<!-- source files: f_0113.xhtml -->

Release It! Second Edition
Chapter
 13
Design for Deployment
In the last chapter, we were stuck in a living nightmare, one of many endless
 deployments that waste countless hours and dollars. Now we turn to sweeter
 dreams as we contemplate automated deployments and even continuous
 deployments. In this chapter you learn how to design your applications for
 easy rollout. Along the way, we look at packaging, integration point
 versioning, and database schemata.

## Chapter 14: Handling Versions

<!-- source files: f_0121.xhtml -->

Release It! Second Edition
Chapter
 14
Handling Versions
We now know how to design applications so that they can be deployed
 easily and repeatedly. That means we also have the ability to change the way
 our software talks with the rest of the world easily and repeatedly. However,
 as we make changes to add features, we need to be careful not to break
 consuming applications. Whenever we do that, we force other teams to do more
 work in order to get running again. Something is definitely wrong if our
 team creates work for several other teams! It’s better for everyone if
 we do some extra work on our end to maintain compatibility rather than
 pushing migration costs out onto other teams. This chapter looks at how your
 software can be a good citizen.

## Chapter 15: Case Study: Trampled by Your Own Customers

<!-- source files: f_0127.xhtml -->

Release It! Second Edition
Chapter
 15
Case Study: Trampled by
Your Own Customers
After years of work, the day of launch finally arrived. I had joined this
 huge team (more than three hundred in total) nine months earlier to help
 build a complete replacement for a retailer’s online store, content
 management, customer service, and order-processing systems. Destined to be
 the company’s backbone for the next ten years, it was already more than a
 year late when I joined the team. For the previous nine months, I had been
 in crunch mode: taking lunches at my desk and working late into the night.
 A Minnesota winter will test your soul even under the best of times. Dawn
 rises late, and dusk falls early. None of us had seen the sun for months.
 It often felt like an inescapable Orwellian nightmare. We had crunched
 through spring, the only season worth living here for. One night I went to
 sleep in winter, and the next time I looked around, I realized summer had
 arrived.
After nine months, I was still one of the new guys. Some of the development
 teams had crunched for more than a year. They had eaten lunches and dinners
 brought in by the client every day of the week. Even today, some of them
 still shiver visibly when remembering turkey tacos.

## Chapter 16: Adaptation

<!-- source files: f_0134.xhtml -->

Release It! Second Edition
Chapter
 16
Adaptation
Change is guaranteed. Survival is not.
You’ve heard the Silicon Valley mantras: “Software is eating the world.”
 “You’re either disrupting the market or you’re going to be disrupted.”
 “Move fast and break things.” What do they all have in common? A total
 focus on change, either on the ability to withstand change or, better yet,
 the ability to create change.
The agile development movement embraced change in response to business
 conditions. These days, however, the arrow is just as likely to point in the
 other direction. Software change can create new products and markets. It can
 open up space for new alliances and new competition, creating surface area
 between businesses that used to be in different industries—like light bulb
 manufacturers running server-side software on a retailer’s cloud computing
 infrastructure.
Sometimes the competition isn’t another firm but yesterday’s version of the
 product, as in the startup realm. You launch your minimum viable product,
 hoping to learn fast, release fast, and find that crucial product-market fit
 before the cash runs out.
In all these cases, we need adaptation. That is the theme we will explore in
 this chapter. Our path touches people, processes, tools,
 and designs. And as you might expect, these interrelate. You’ll need to introduce
 them in parallel and incrementally.

## Chapter 17: Chaos Engineering

<!-- source files: f_0140.xhtml -->

Release It! Second Edition
Chapter
 17
Chaos Engineering
Imagine a conversation that starts like this:
“Hey boss, I’m going to log into production and kill some boxes. Just a
 few here and there. Shouldn’t hurt anything,” you say.
How do you think the rest of that conversation will go? It might end up
 with a visit from Human Resources and an order to clean out your
 desk. Maybe even a visit to the local psychiatric facility!
 Killing instances turns out to be a radical idea—but not a crazy
 one. It’s one technique in an emerging discipline called “chaos
 engineering.”

## Extracted Source Map

| Chapter | Title | Lines | Original EPUB entries |
|---:|---|---:|---|
| 1 | Chapter 1: Living in Production | 8-47 | f_0010.xhtml |
| 2 | Chapter 2: Case Study: The Exception That Grounded an Airline | 48-108 | f_0018.xhtml |
| 3 | Chapter 3: Stabilize Your System | 109-165 | f_0026.xhtml |
| 4 | Chapter 4: Stability Antipatterns | 166-254 | f_0033.xhtml |
| 5 | Chapter 5: Stability Patterns | 255-279 | f_0047.xhtml |
| 6 | Chapter 6: Case Study: Phenomenal Cosmic Powers, Itty-Bitty Living Space | 280-339 | f_0063.xhtml |
| 7 | Chapter 7: Foundations | 340-399 | f_0074.xhtml |
| 8 | Chapter 8: Processes on Machines | 400-490 | f_0078.xhtml |
| 9 | Chapter 9: Interconnect | 491-511 | f_0083.xhtml |
| 10 | Chapter 10: Control Plane | 512-536 | f_0092.xhtml |
| 11 | Chapter 11: Security | 537-576 | f_0104.xhtml |
| 12 | Chapter 12: Case Study: Waiting for Godot | 577-689 | f_0112.xhtml |
| 13 | Chapter 13: Design for Deployment | 690-704 | f_0113.xhtml |
| 14 | Chapter 14: Handling Versions | 705-723 | f_0121.xhtml |
| 15 | Chapter 15: Case Study: Trampled by Your Own Customers | 724-750 | f_0127.xhtml |
| 16 | Chapter 16: Adaptation | 751-780 | f_0134.xhtml |
| 17 | Chapter 17: Chaos Engineering | 781-798 | f_0140.xhtml |
