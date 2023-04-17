# IS597_Project_WBC_Simulation

## Team Member
Cindy Yang(tyy0309), Judy Chan(iamjudy)

## Background
![image](https://user-images.githubusercontent.com/109567215/232337806-4c6040cd-d755-4170-bf17-2fb7174c0d36.png)

Our project focuses on the 2023 World Baseball Classic (WBC) and aims to investigate the impact of **different competition formats** and **pitching roles** on game outcomes. The WBC has undergone significant changes in its tournament format over the past five editions. In 2006, the tournament featured round-robin group play in the first and second rounds, followed by single-elimination semifinals and finals. In 2009, the format was modified to a double-elimination system for the first two rounds (with the semifinals and final remaining single-elimination), which replaced the controversial round-robin format. In 2013, the tournament returned to a round-robin format for the first round, with the second round remaining double-elimination. In 2017, the format reverted to that of 2006, with both the first and second rounds being round-robin. For 2023, the tournament will feature a round-robin format in the first round, followed by single-elimination for the rest of the competition. By analyzing these various formats and the impact of pitching roles, we hope to gain insights into their effects on game results.

## Hypothesis
  - The more pitches the starting pitcher throws, the higher the probability of winning.
  - The round-robin format is more advantageous for teams with stable performance than the single-elimination format.
  
## Assumptions
  - The simulation will focus on the quarterfinals and beyond to simplify the analysis. The finals will remain single-elimination.
  - To generate WBC data, we will use MLB data, as it is more widely available online.
  - We assume that when the starting pitcher throw more pitches, it will decrease the number of pitches thrown by other pitchers in the same game.
  - The simulation will consider only average pitcher and batter performance, competition system, and pitching limitations, and exclude factors such as weather and home team advantage.
  - Stable performance can be represented by the standard deviation of the win rate for each game.
  - If the points are tied in the round-robin, the ranking will be determined by the "run rate" (total runs allowed / total number of outs) among teams with the same record.
  
## Phase 1 - Random Variables

## Phase 2 & 3 - Controls & Experiments


## References
  - World Baseball Classic data
  https://www.mlb.com/world-baseball-classic/stats/team/runs
  - World Baseball Classic wikipedia
  https://en.wikipedia.org/wiki/2023_World_Baseball_Classic