# Testing Circom Repository

This repository is a workplace aimed to store tutorials and basic implementations of the ROLLUP zero knowledge approach for the Blockchain environment.

## (1) RollupNC with Circom, SnarkJS

A very useful and straightforward tutorial.

Cons: It uses a deprecated version of Circom & SnarkJS

Link: https://github.com/therealyingtong/roll_up_circom_tutorial

## (2) Setting Up Circom - Be Careful !

This tutorial was a nightmare to setup. Repo's owner was not at fault, but the developers at @iden3 were.
Circom is an extremely useful library to implement arithemtic circuit aimed at a zkSNARK implementation.
The real problem lives beneath the maintenance and support over the variuos Circom@versions.
Basically, as they say, there are two distinct and separate Circom Libraries:

- Circom < 2.0.0 : written in JavaScript and mostly used from tutorial available online.
- Circom 2.0.0 : written in Rust, with smaller but substantial changes form the versions already published.

Due to the drastic change of structure, collateral damage is inevitable. _Each version of the Circom Library has merely the same commands and outcomes, so be careful._

Before compiling any _file.circom_ into your library, follow these steps:

1. Check your global circom version

   > circom --version

   and see if it matches with the tutorial's one. If not, then uninstall it globally, either via _npm_ or from your Rust Cargo global path.

   > (UNIX) sudo npm uninstall -g circom

2. Proceed to install the _right_ version of circom:
   > (UNIX) sudo npm install -g circom@version

Personally, I would recommend to study upon the newest version of Circom, but you can easily transition from the dperecated ones, to the 2.0.0 pretty easily. Just check the projects version and install only that one version into your PC or Local Repository.

TO RUN CIRCOM INTO FOLDER: $(npm bin)/circom
