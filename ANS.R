install.packages(c("tidygraph", "ggraph", "sna", "visNetwork", "networkD3", "caret"))

library(compiler)
library(dplyr)
library(tidygraph)
library(ggraph)
library(tidyverse)
library(sna)
library(igraph)
library(visNetwork)
library(networkD3)
library(caret)

lineup <- read_csv("lineups.csv")
lineup$id <- lineup$id +1 
names(lineup) <- c('id','label','team')

matchups <- read_csv("matchups.csv")
matchup <- matchups[,c("home_players","away_players","type","weight","home_team","away_team","time")]
names(matchup) <- c('from','to','weight','score',"home_team","away_team","time")
matchup$to <- matchup$to+1
matchup$from <- matchup$from+1
matchup <- matchup[!(matchup$weight==0),]


#consider time effect
matchup$score_adjusted <- matchup$score/matchup$time 

matchup$weight <- factor(matchup$weight)

print(paste("# Lineups: ",nrow(lineup)))
print(paste("# Matchups: ",nrow(matchups)))
print(paste("# Matchups after filtering: ",nrow(matchup),"(differences:",nrow(matchups)-nrow(matchup),")"))

matchup_plot <- matchup
basenet <- tbl_graph(nodes = lineup, edges = matchup_plot, directed = T,node_key = "label")
basenet

basenet %>% activate(nodes) %>%  as_tibble() %>%
  group_by(team)%>%
  summarise(count = n() ) %>% arrange(count) -> n_lineups

n_lineups

pdegree <- basenet %>% 
  activate(edges) %>% filter(weight == 1) %>%
  activate(nodes) %>%
  mutate(
    Pin = centrality_degree(mode = "in"),
    Pout = centrality_degree(mode = "out")
  )  %>%
  as_tibble()

ndegree <- basenet %>% activate(edges) %>% filter(weight == -1) %>%
  activate(nodes) %>%
  mutate(
    Nin = centrality_degree(mode = "in"),
    Nout = centrality_degree(mode = "out"),
    #   degree = centrality_degree(mode = "all")
  ) %>%
  as_tibble()

new_lineup <- inner_join(pdegree,ndegree,by=c("id","label","team"))

basenet %>% 
  activate(nodes) %>%
  mutate(
    in_degree = centrality_degree(mode = "in"),
    out_degree = centrality_degree(mode = "out"),
    degree = centrality_degree(mode = "all")
  ) %>%
  as_tibble()


pairs <- matchup %>% distinct(from, to, .keep_all = F)
edge_centric <- data.frame(node1=numeric(), node2=numeric(),
                           Pin_Pout=numeric(), Pin_Nout=numeric(), Nin_Pout=numeric(), Nin_Nout=numeric(),
                           Pin_Pin=numeric(), Pin_Nin=numeric(), Nin_Pin=numeric(), Nin_Nin=numeric(),
                           Pout_Pin=numeric(), Pout_Nin=numeric(), Nout_Pin=numeric(), Nout_Nin=numeric(),
                           Pout_Pout=numeric(), Pout_Nout=numeric(), Nout_Pout=numeric(), Nout_Nout=numeric(),
                           stringsAsFactors=FALSE)

# input
name_list <- names(edge_centric)[3:18] 

# mapping
map <- c(
  "Pin_Pout" = c(1,1), "Pin_Nout" = c(1,-1), "Nin_Pout" = c(-1,1), "Nin_Nout" = c(-1,-1),
  "Pin_Pin"= c(1,1),    "Pin_Nin"= c(1,-1),    "Nin_Pin"= c(-1,1),  "Nin_Nin"= c(-1,-1),   
  "Pout_Pin"= c(1,1),   "Pout_Nin"= c(1,-1),   "Nout_Pin"= c(-1,1),  "Nout_Nin"= c(-1,-1),
  "Pout_Pout"= c(1,1),  "Pout_Nout"= c(1,-1),  "Nout_Pout"= c(-1,1), "Nout_Nout"= c(-1,-1)
)

map[paste(name_list[1],1,sep="")] 
map[paste(name_list[1],2,sep="")]

edge_centric <- read.csv("edge_centric.csv")


# group by absolute scores
#distinct_matchup <- matchup %>% 
#  group_by(from, to) %>%                            
#  summarise(score = sum(score)) %>%
#  mutate(result = sign(score)) %>% ungroup()


# group by absolute scores
distinct_matchup <- matchup %>% 
  group_by(from, to) %>%                            
  summarise(score_adjusted = sum(score_adjusted)) %>%
  mutate(result = sign(score_adjusted)) %>% ungroup()


print(nrow(distinct_matchup))
print(nrow(edge_centric))

# Data
data <- edge_centric %>% inner_join(distinct_matchup,by=c("node1"="from","node2"="to"))
#data <- edge_centric_undir %>% inner_join(distinct_matchup,by=c("node1"="from","node2"="to"))
data$result <- ifelse(data$result==1,"win","loss")
# Inspect the data
sample_n(data, 3)

# Split the data into training and test set
set.seed(1)
training.samples <- data$result %>% 
  createDataPartition(p = 0.9, list = FALSE)
train.data  <- data[training.samples, ]
test.data <- data[-training.samples, ]

# The first 80% of matchups will be used for training, rest for testing (since we want to predict future results)
trainPrecentage <- 0.8
train.data <- data[1:floor(0.8*nrow(data)),]
test.data <- data[(floor(0.8*nrow(data))+1):nrow(data),]

trainDataScaled <- train.data
testDataScaled <- test.data

# Scale data into uniform interval
trainDataScaled[c(3:18)] <- scale(trainDataScaled[c(3:18)])
testDataScaled[c(3:18)] <- scale(testDataScaled[c(3:18)])

trainDataScaled$result <- ifelse(trainDataScaled$result=="win", 1, 0)
testDataScaled$result <- ifelse(testDataScaled$result=="win", 1, 0)

trainDataScaled <- replace(trainDataScaled, is.na(trainDataScaled), 0)
testDataScaled <- replace(testDataScaled, is.na(testDataScaled), 0)

install.packages(c("mlegp", "caTools", "kernlab"))

# May need to install some more packages
library(mlegp)
library(caTools) 
library(kernlab)

set.seed(1)
model <- gausspr(result ~ Pin_Pout+Pin_Nout+Nin_Pout+Nin_Nout+Pin_Pin+Pin_Nin+Nin_Pin+Nin_Nin+Pout_Pin+Pout_Nin+Nout_Pin+Nout_Nin+Pout_Pout+Pout_Nout+Nout_Pout+Nout_Nout, data=trainDataScaled, kernel="vanilladot")
summary(model)

y_pred = predict(model, testDataScaled)

print("Gaussian Process Accuracy: ")
print(mean(y_pred == testDataScaled$result))

# Further kernels
gpKernels = c("rbfdot", "anovadot", "laplacedot")

for (i in gpKernels){
  set.seed(1)
  
  model <- gausspr(result ~ Pin_Pout+Pin_Nout+Nin_Pout+Nin_Nout+Pin_Pin+Pin_Nin+Nin_Pin+Nin_Nin+Pout_Pin+Pout_Nin+Nout_Pin+Nout_Nin+Pout_Pout+Pout_Nout+Nout_Pout+Nout_Nout, data=trainDataScaled, kernel=i)
  summary(model)
  
  y_pred = predict(model, testDataScaled)
  
  print("Kernel:")
  print(i)
  print("Gaussian Process Accuracy: ")
  print(mean(y_pred == testDataScaled$result))
}