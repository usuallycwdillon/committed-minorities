# Analysis of the data from the 'committed-minorities' simulation project
# 
# The poweRlaw package (Gillespie) has some easy to use methods for modeling 
# power law distributions in data, plotting them using standard R plot commands
# and ---maybe most importantly--- comparing the power law fit to a log-normal 
# model fit (and poisson models, but I didn't really use that).


library("poweRlaw", lib.loc="/usr/lib64/R/library")

i_data <- read.csv("~/Code/committedMinorities/committed-minorities/data/iGraph_2014-07-29 194833:.csv")
i_data07 <- read.csv("~/Code/committedMinorities/committed-minorities/data/iGraph_2014-07-30 133925:.csv")
i_data50 <- read.csv("~/Code/committedMinorities/committed-minorities/data/iGraph_2014-07-30 134529:.csv")
i_data80 <- read.csv("~/Code/committedMinorities/committed-minorities/data/iGraph_2014-07-30 134501:.csv")
i_data90 <- read.csv("~/Code/committedMinorities/committed-minorities/data/iGraph_2014-07-30 134519:.csv")
i_data99 <- read.csv("~/Code/committedMinorities/committed-minorities/data/iGraph_2014-07-30 135752:.csv")

n_data <- read.csv("~/Code/committedMinorities/committed-minorities/data/nGraph_2014-07-29 195206:.csv")

# length(i_data[,1])
# length(i_data07[,1])
# length(i_data50[,1])
# length(i_data80[,1])
# length(i_data90[,1])
# length(i_data99[,1])
# 
# length(n_data[,1])
# 
# plot(i_data$A.ratio)
# plot(i_data$AB.ratio)
# plot(i_data$B.ratio)
# 
# plot(i_data07$A.ratio)
# plot(i_data07$AB.ratio)
# plot(i_data07$B.ratio)
# 
# plot(i_data50$A.ratio)
# plot(i_data50$AB.ratio)
# plot(i_data50$B.ratio)
# 
# plot(i_data80$A.ratio)
# plot(i_data80$AB.ratio)
# plot(i_data80$B.ratio)
# 
# plot(i_data90$A.ratio)
# plot(i_data90$AB.ratio)
# plot(i_data90$B.ratio)
# 
# plot(i_data99$A.ratio)
# plot(i_data99$AB.ratio)
# plot(i_data99$B.ratio)
# 
# plot(n_data$A.ratio)
# plot(n_data$AB.ratio)
# plot(n_data$B.ratio)

# power law fit testing
# The node counts are really discrete counts 0 - 1,000 so I use poweRlaw's 'displ' methods. To do that, though, I multiply the data by 1000 and slice the zeros out of the vector. 
 
ia99 <- i_data99$A.ratio * 1000
ia99k <- ia99[1:106]

m_pl99 <- displ$new(ia99k) # this is the discrete power law model
ep99 <- estimate_xmin(m_pl99) # X min estimate, 9 and scaling parameter 1.3232
                             # by MLE. K-S fit is only .2364, however.

# Xie, et al also say that node degree decreases (probability of an edge, in 
# my case) then the model devolves to something more like a lognormal model.
m_ln99 <- dislnorm$new(ia99k)
el99 <- estimate_xmin(m_ln99)


# The next steps will require establishing the model parameters
m_pl99$setXmin(ep99)
m_ln99$setXmin(el99)


# We compare these models against the data visually
plot(m_pl99, 
     ylab="CDF", 
     xlab="Nodes with Initial Opinion", 
     main="Consensus Times with Near-Connectedness (python)")
lines(m_pl99, col=2)
lines(m_ln99, col=3)

# Both models seem to fit the data, visually. Closer examination is needed, so
# I use poweRlaw's 'compare_distributions' method:
m_lnn$setXmin(m_pln$getXmin())

est <- estimate_pars(m_lnn)
m_lnn$setPars(est)

comp_pl_ln <-  compare_distributions(m_pln, m_lnn)
comp_pl_ln


# Next, I want to compare to the E(1000, 0.03) graphs by iGraph and Neo4j models

# The iGraph model is i_data
ia <- i_data$A.ratio * 1000
iak <- ia[1:185]

m_pli <- displ$new(iak) # this is the discrete power law model
epi <- estimate_xmin(m_pli) 

# Xie, et al also say that node degree decreases (probability of an edge, in 
# my case) then the model devolves to something more like a lognormal model.
m_lni <- dislnorm$new(iak)
eli <- estimate_xmin(m_lni)


# The next steps will require establishing the model parameters
m_pli$setXmin(epi)
m_lni$setXmin(eli)

# We compare these models against the data visually
plot(m_pli, 
     ylab="CDF", 
     xlab="Nodes with Majority Opinion", 
     main="Consensus Times with 3% \n Probability of Connectedness (iGraph)")
lines(m_pli, col=2)
lines(m_lni, col=3)


m_lni$setXmin(m_pli$getXmin())

est <- estimate_pars(m_lni)
m_lni$setPars(est)

comp_pl_ln <-  compare_distributions(m_pli, m_lni)
comp_pl_ln

######################################################
# 

ib <- i_data$B.ratio * 1000
ibk <- ib[1:185]

m_pli <- displ$new(ibk) # this is the discrete power law model
epi <- estimate_xmin(m_pli) 

# Xie, et al also say that node degree decreases (probability of an edge, in 
# my case) then the model devolves to something more like a lognormal model.
m_lni <- dislnorm$new(ibk)
eli <- estimate_xmin(m_lni)


# The next steps will require establishing the model parameters
m_pli$setXmin(epi)
m_lni$setXmin(eli)


# We compare these models against the data visually
plot(m_pli, 
     ylab="CDF", 
     xlab="Nodes with Minority Opinion", 
     main="Consensus Times with 3% \n Probability of Connectedness (iGraph)")
lines(m_pli, col=2)
lines(m_lni, col=3)

# Compare power law fit to log-normal fit
m_lni$setXmin(m_pli$getXmin())

est <- estimate_pars(m_lni)
m_lni$setPars(est)

comp_pl_ln <-  compare_distributions(m_pli, m_lni)
comp_pl_ln


################################################################################
# The Neo4j model is n_data
na <- n_data$A.ratio * 1000
nak <- na[1:126]

m_pln <- displ$new(nak) # this is the discrete power law model
epn <- estimate_xmin(m_pln) 

# Xie, et al also say that node degree decreases (probability of an edge, in 
# my case) then the model devolves to something more like a lognormal model.
m_lnn <- dislnorm$new(nak)
eln <- estimate_xmin(m_lnn)


# The next steps will require establishing the model parameters
m_pln$setXmin(epn)
m_lnn$setXmin(eln)


# We compare these models against the data visually
plot(m_pln, 
     ylab="CDF", 
     xlab="Nodes with Majority Opinion", 
     main="Consensus Times with 3% \nProbability of Connectedness (Neo4j)")
lines(m_pln, col=2)
lines(m_lnn, col=3)

m_lnn$setXmin(m_pln$getXmin())

est <- estimate_pars(m_lnn)
m_lnn$setPars(est)

comp_pl_ln <-  compare_distributions(m_pln, m_lnn)
comp_pl_ln

###########################
# Nodes with minority opinion
nb <- n_data$B.ratio * 1000
nbk <- nb[1:180] 

m_pln <- displ$new(nbk) # this is the discrete power law model
epn <- estimate_xmin(m_pln) 

m_lnn <- dislnorm$new(nbk)
eln <- estimate_xmin(m_lnn)

# The next steps will require establishing the model parameters
m_pln$setXmin(epn)
m_lnn$setXmin(eln)

# We compare these models against the data visually
plot(m_pln, 
     ylab="CDF", 
     xlab="Nodes with Minority Opinion", 
     main="Consensus Times with 3% Probability of Connectedness (Neo4j)")
lines(m_pln, col=2)
lines(m_lnn, col=3)

###################################
# python minority opinion consensus

# m_lnn$setXmin(m_pln$getXmin())
# 
# est <- estimate_pars(m_lnn)
# m_lnn$setPars(est)
# 
# comp_pl_ln <-  compare_distributions(m_pln, m_lnn)
# comp_pl_ln

#############################
# Nodes with both opinions
nab <- n_data$AB.ratio * 1000
nabk <- nab[1:179]

m_pln <- displ$new(nabk) # this is the discrete power law model
epn <- estimate_xmin(m_pln) 

# Xie, et al also say that node degree decreases (probability of an edge, in 
# my case) then the model devolves to something more like a lognormal model.
m_lnn <- dislnorm$new(nabk)
eln <- estimate_xmin(m_lnn)

# The next steps will require establishing the model parameters
m_pln$setXmin(epn)
m_lnn$setXmin(eln)

# We compare these models against the data visually
plot(m_pln, 
     ylab="CDF", 
     xlab="Nodes with Both Opinions", 
     main="Consensus Times with 3% Probability of Connectedness (Neo4j)")
lines(m_pln, col=2)
lines(m_lnn, col=3)

############################
# From the manual, this is a reasonable way to compare models
m_lnn$setXmin(m_pln$getXmin())

est <- estimate_pars(m_lnn)
m_lnn$setPars(est)

comp_pl_ln <-  compare_distributions(m_pln, m_lnn)
comp_pl_ln


################################################################################
# Get citations and create bibtext for them

toBibtex(citation("base"))
toBibtex(citation("igraph"))
toBibtex(citation("poweRlaw"))




