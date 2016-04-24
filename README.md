# Enginous

An easy-to-use search tool for databases of designs.

## Motivation

As part of my research into design automation, I feel there need to be more tools that encourage fast, prototype-driven use of computers in engineering.  In doing this, one challenge we've kept running into is the tradeoff between speed of development, speed of use, and reliability of the results.  In terms of reliability and speed of development, we generally choose to make "foward" models (that is, a model that takes a design and predicts performance) in a high level (and slow-performing) language.  When we are designing, we generally want one of two things from these computer tools: either to explore a wide range of "different" designs in search of inspiration or a unique angle, or to find a single, specific design that gives us the performance we desire.

Combining these two thoughts, it's relativly fast and easy to build a database of designs offline-the task is generally trivially parallelizable.  We want a way to find designs in this database that give us a certain performance.  Lots of people have developed cool methods of approximating that inverse function, such as neural networks and meta-modelling, but I wanted to make something simpler to use and more general, albeit slower and probably more memory-intensive

## How it works

We require two features of the designs: that the distance between two designs can be calculated, and that the triangle inequality holds over that distance.  In our use that distance is generally calculated off of performance, so we are searching for designs with a certain performance.

We use Shapiro's algorithm, with a few additions.  The algorithm works by precalculating several "landmark" points, and calculating the distances from the landmarks to every other point in the database.  When searching for a design, we calculate the distance from our target to the landmarks, locate the "nearest" landmark, then throw out any points in the db whose distance to the landmark is more than twice that of the target.

One we've filtered the set of points, we iterate over the remaining points in the db, in order of increasing difference between the target distance and design distance.

For calculating the landmarks, we use a bootstrapping approach to estimate the expected number of points that can be filtered given a certain number of landmarks.  This way, the operator can decide the space-time tradeoffs they want to make.

## To Do

Allow easy parallelization and distribution of the search activity.
