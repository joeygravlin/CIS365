<div class="container-fluid">

<div class="navbar-header">

<span class="sr-only">Toggle navigation</span>
<span class="icon-bar"></span> <span class="icon-bar"></span>
<span class="icon-bar"></span>

[![university image](static/gvsu_logo.png)](../../index.html)

</div>

<div id="course-information-header" class="collapse navbar-collapse">

<div class="course-title-header">

[CIS 365 - Artificial Intelligence
Winter 2018](http://www.cis.gvsu.edu/~moorejar/WS18_CIS365)

</div>

</div>

</div>

<div class="container">

<div class="row">

<div class="col-sm-3">

<div class="navbar-header">

<span class="sr-only">Toggle navigation</span>
<span class="icon-bar"></span> <span class="icon-bar"></span>
<span class="icon-bar"></span>

</div>

<div class="collapse navbar-collapse navbar-ex1-collapse">

  - [Syllabus](./syllabus.html)
  - [Schedule](./schedule.html)
  - [Study Guide](./study_guide.html)
  - [Command Line](./linux_command_line_overview.html)
  - [Presentation Guidelines](./project_3_presentation_rubric.html)
  - [Assignments <span class="caret"></span>](#)
      - [Individual Assignment \#1: Review a recent AI Paper and Provide
        Commentary](assign_1.html)
  - [Projects <span class="caret"></span>](#)
      - [Project \#1: Building AI Foundations](project_1.html)

</div>

</div>

<div class="col-sm-9">

<div class="header">

# CIS 365 - Artificial Intelligence

# Winter 2018

</div>

<div class="row">

<div class="col-sm-12">

### Project \#1: Building AI Foundations

#### Creating Game Playing Agents

This project introduces you to some of the strategies and environments
encountered in the field of Artificial Intelligence. Although we haven't
covered techniques yet, your goal will be to gain familiarity with
interpreting sensor data about the world, coordinating a swarm of
agents, and, hopefully, winning a game of [Halite](https://halite.io/)
against other players.

As it is early in the course, I do not expect you to develop new AI
algorithms, but rather, (1) try to come up with strategies that perform
well in the game world and (2) reflect on why things work, or do not. In
doing so, you will learn how to interpret external information about an
environment and apply it to the behavior of your individual agents.
Halite is a 2D game world with the goal to defeat your enemies or
capture as many planets as possible within a single game.

#### Basic Game Description:

Halite is played on a 2D board comprised of space and planets. Players
must capture and mine planets with their initial ships to produce
additional ships to expand, combat, and conquer new territory. Planets
are unowned until claimed by players.

This year's competition is focused on pathfinding and decision making.
You must code behaviors that value exploration (finding new planets),
exploitation (mining planets you currently own) and combat (fight other
players). **Information on the game world, rules, and objectives are
found here:**
[](https://halite.io/learn-programming-challenge/basic-game-rules/)<https://halite.io/learn-programming-challenge/basic-game-rules/>

#### Problem Statement:

In this project, you will build a game playing agent and compete against
the online community and your peers at the end.

Grading is detailed below, but will be based on:

1.  The quality of your code.
2.  How well your bot competes against your peers.
3.  A two-three page writeup detailing your team's experience.

At the end of the project, I will conduct a tournament between all
submitted bots for a final ranking.

#### Getting Started:

Getting started can be a bit daunting, but I recommend looking into the
following:

  - Sentdex Tutorial Videos:
    [here](https://www.youtube.com/watch?v=QjAu5lJo4zs)
  - Halite Developer Blog:
    [here](https://forums.halite.io/t/how-do-i-get-started-with-halite-as-a-beginner/517)
  - Halite Basic Game Rules:
    [here](https://halite.io/learn-programming-challenge/basic-game-rules/)
  - Halite Design Principles:
    [here](https://halite.io/learn-programming-challenge/other-resources/design-principles-underlying-halite-II)
  - The Halite forums contain a wealth of information these two threads
    are potentially informative: [here](https://forums.halite.io/)
  - View strategies of the best players by checking the leaderboard and
    clicking on a user:
    [here](https://halite.io/programming-competition-leaderboard)

Local Visualizers are plentiful on the forums. Here is one
[visulizer](https://github.com/fohristiwhirl/chlorine). I encourage you
to look for others if you want to view your results offline.

Use the Python3 starter kit that can be downloaded
[here](https://halite.io/learn-programming-challenge/downloads-and-starter-kits/).

Command reference for running locally
[here](https://halite.io/learn-programming-challenge/halite-cli-and-tools/cli).

#### Learning Objectives:

1.  Become familiar working with sensor data and using it to shape
    behavior.
2.  Gain experience with Python AI programming.
3.  Develop techniques to shape behavior of a swarm of agents in a
    world.

#### Rubric:

As noted earlier, you will be graded on:

1.  The quality of your code.
2.  How well your bot competes against your peers.
3.  A two-three page writeup detailing your team's experience.

Your writeup will be graded on the quality of the writing, and a
discussion about your experience with this project. Some of the
following questions may help you get started with the writeup, but I
leave it open to the group to decide what format and structure to take.

1.  What strategy(s) did you employ with your swarms?
2.  What behaviors did you implement?
3.  What worked? What didn't?
4.  Speculate as to why your bot was effective against some opponents
    but not others.
5.  What was difficult?
6.  What was fun?
7.  Was there anything that was particularly frustrating, and how could
    it be fixed in the future?
8.  If you tried a novel behavior and it fails spectacularly, did it
    accomplish what you set out to do? (e.g. zerg rushing at the start,
    always go for fringe planets, etc)  
    *If you gained insight or code from online sources, please list and
    briefly discuss why you chose to use it and what contribution to
    your final bot the code made.* *Illustrations and/or screenshots are
    encouraged if they integrate well with the text. Excessive
    screenshots do not contribute to the document length.*

Well documented code is essential to good development practices. Make
sure to document any new code you added, including sources for
inspiration or even where a new component was found. Clearly, and
concisely explain what the code does, how does it do it, and how does it
fit with your bot's behavior.

I reserve the right to award flex points for exemplary work in any areas
of this project, including, but not limited to creative algoritms or
behaviors, performance on the public leaderboard,
etc.

<div class="grading-table">

<div>

</div>

| Category                  | Rubric                         | Max Score |
| ------------------------- | ------------------------------ | --------- |
| Performance Against Peers |                                |           |
|                           | Bottom 4                       | 2         |
|                           | Middle 4                       | 4         |
|                           | Top 5                          | 6         |
|                           | Top 1                          | 10        |
| Writeup and Exploration   |                                |           |
|                           | Minimal                        | 45        |
|                           | Moderate                       | 50        |
|                           | Good                           | 55        |
|                           | Comprehensive                  | 60        |
|                           | Exemplary                      | 62        |
| Code and Documentation    |                                |           |
|                           | Not Functioning                | 0         |
|                           | Assuming Functional            | ...       |
|                           | No Documentation               | 18        |
|                           | Minimal Documentation          | 23        |
|                           | Overly Documented              | 25        |
|                           | Clear, Concise Documentation   | 28        |
| Flex Points               |                                |           |
|                           | Creative Algorithm/Behaviors   | 5         |
|                           | Public Leaderboard Performance | 5         |
|                           | *Reserved*                     | 5         |

</div>

#### Deliverables

Submit the following through Blackboard's Assignment Manager. One
submission per group. Please include in the comments section of the
assignment the names of the group members.

1.  Your Final Bot Code, filename specification:
    'teamname\_final\_bot.py'.
2.  Write up (single-spaced) detailing the your team's experiences. See
    description above.
3.  Readme file containing the names of the group members.

</div>

</div>

</div>

<div class="container text-center">

-----

<div class="row">

<div class="col-sm-3">

  - [© 2016 Jared Moore](/)

</div>

<div class="col-sm-3">

  - [About Me](http://www.jaredmmoore.com)

</div>

<div class="col-sm-3">

  - [Github
    Repository](https://github.com/jaredmoore/Default_Course_Tempalte)

</div>

</div>

</div>

</div>

</div>
