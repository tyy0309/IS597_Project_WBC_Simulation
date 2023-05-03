# IS597_Project_WBC_Simulation

## Team Member
Cindy Yang (tyy0309), Judy Chan (iamjudy)

## Background
![image](https://user-images.githubusercontent.com/109567215/232337806-4c6040cd-d755-4170-bf17-2fb7174c0d36.png)

Our project focuses on the 2023 World Baseball Classic (WBC) and aims to investigate the impact of **different competition formats** and **pitching roles** on game outcomes. The WBC has undergone significant changes in its tournament format over the past five editions. In 2006, the tournament featured round-robin group play in the first and second rounds, followed by single-elimination semifinals and finals. In 2009, the format was modified to a double-elimination system for the first two rounds (with the semifinals and final remaining single-elimination), which replaced the controversial round-robin format. In 2013, the tournament returned to a round-robin format for the first round, with the second round remaining double-elimination. In 2017, the format reverted to that of 2006, with both the first and second rounds being round-robin. For 2023, the tournament will feature a round-robin format in the first round, followed by single-elimination for the rest of the competition. By analyzing these various formats and the impact of pitching roles, we hope to gain insights into their effects on game results.

## Experiment 1
### Hypothesis
The more pitches the starting pitcher throws, the higher the probability of winning.
  
### Assumptions
  - The simulation will focus on the quarterfinals to simplify the analysis.
  - We assume that when the starting pitcher throw more pitches, it will decrease the number of pitches thrown by other pitchers in the same game.
  - The simulation will consider only average pitcher and batter performance, competition system, and pitching limitations, and exclude factors such as weather and home team advantage.
  - Stable performance can be represented by the standard deviation of the win rate for each game.
  - If the points are tied in the round-robin, the ranking will be determined by the "run rate" (total runs allowed / total number of outs) among teams with the same record.
  
### Phase 1 - Design
We have decided on the following formulas to determine the team's performance:

$$\text{Total Performance}= \text{Pitching Score} + \text{Hitting Score}$$

$$\text{Pitching Score}=(0.3 \times \text{ERA}) + (0.25 \times \text{WHIP}) + (0.15 \times \text{BAA}) + (0.1 \times \text{IP})+ (0.2 \times \text{K})$$

$$\text{Hitting Score}=(0.25 \times \text{BA}) + (0.3 \times \text{OPS}) + (0.15 \times \text{RBI}) + (0.1 \times \text{BB}) + (0.1 \times \text{SO}) + (0.1 \times \text{SB})$$

> **Note**: Since each statistic can have different scales and interpretations (higher values may represent better performance for some indicators and worse performance for others), we will use normalization in our code to process these values. We will transform each score into a range between 0 and 1.

**Random Variables**:
1. At the beginning of each game simulation, players are selected at random as follows：
    - Randomly select 3 pitchers from `data/pitchers.csv`
    - Randomly select 9 batters from `data/batters.csv`

2.  Generating Normally Distributed Simulation Data Based on Season Performance
    
    Since we are referencing data from an entire season, but player performance should fluctuate, when selecting players, we will generate normally distributed game data based on the user input number of simulations, and ensure that the mean of these values matches the overall performance for the season 

    For example, if player A has a batting average of 0.3 for the entire season and 100 games are simulated, random values `x1` to `x100` of batting averages will be generated, following a normal distribution, and $$\frac{1}{100}\sum_{i=1}^{100}x_i = 0.3$$

3. Randomly allocate the number of pitches for the three pitchers and use them as weights when calculating performance scores:

$$\text{Pitching Score}=(0.3 \times \text{ERA}) + (0.25 \times \text{WHIP}) + (0.15 \times \text{BAA}) + (0.1 \times \text{IP})+ (0.2 \times \text{K})$$

$$\text{Pitching Score} = (\text{p1-pitch-count}/\text{total-pitch-count}) \times \text{p1} + (\text{p2-pitch-count}/\text{total-pitch-count}) \times \text{p2} + \(\text{p3-pitch-count}/\text{total-pitch-count}) \times \text{p3}$$
  
  
### Phase 2 - Validation
**Comparing Simulation Results to 2023 WBC Rankings**:

We will compare our simulation results to the actual rankings of the 2023 WBC to see if they align with reality. The top eight teams in the competition are as follows:

1. Japan (JPN)
2. United States (USA)
3. Mexico (MEX)
4. Cuba (CUB)
5. Venezuela (VEN)
6. Puerto Rico (PUR)
7. Australia (AUS)
8. Italy (ITA)

By analyzing our simulation results, we can determine if our model accurately predicts the performance of these teams.


### Phase 3 - Experiment
**Two teams with similar strengths**
  - By observing the conditional probability (i.e., the probability of Team A winning when their starting pitcher has a higher pitch count), it can be inferred that when the starting pitcher has a higher pitch count, the team is more likely to win.

**Two teams with a significant difference in strength**
  - When observing the conditional probability, it can be noticed that for the stronger team, the number of pitches thrown by the starting pitcher does not have a significant impact on the win rate. However, for the weaker team, a large proportion of their wins occur when their starting pitcher throws more pitches than the starting pitcher of the stronger team.



## Experiment 2
### Hypothesis
The round-robin format is more advantageous for teams with stable performance than the single-elimination format.
  
### Assumptions
- The simulation will focus on the quarterfinals and beyond to simplify the analysis. The finals will remain single-elimination.
- To generate WBC data, we will use MLB data, as it is more widely available online.
- We assume that when the starting pitcher throw more pitches, it will decrease the number of pitches thrown by other pitchers in the same game.
- The simulation will consider only average pitcher and batter performance, competition system, and pitching limitations, and exclude factors such as weather and home team advantage.
- Stable performance can be represented by the standard deviation of the win rate for each game.
- If the points are tied in the round-robin, the ranking will be determined by the "run rate" (total runs allowed / total number of outs) among teams with the same record.

## References
  - World Baseball Classic data
  https://www.mlb.com/world-baseball-classic/stats/team/runs
  - World Baseball Classic wikipedia
  https://en.wikipedia.org/wiki/2023_World_Baseball_Classic
