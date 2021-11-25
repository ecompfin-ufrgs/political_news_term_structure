Empirical Strategy
==================

Data
^^^^

First, we measure the phenomena we want to observe. In our case, this means collecting data on the term structure 
and on political events. The interest rate from which the term structure we will consider is the one day inter-bank
deposits rate (DI rate). From the DI rate we will collect both the one-day rate and its futures. We choose this
specific interest rate as it is backed by public titles and defined by competition across banks as they lend from
and borrow to each other with the intention of not closing with negative cash. This rate also is the asset behind a
lot of post-fixed income contracts.

In order to measure political events we collect political news data from Brazilian news portals,
so we can calculate the volume of political news and use it as a proxy for political events.
We will collect only the main information about each article (date and time, title and link).
The news portals will be chosen considering their importance and the availability of data on each
one (which will be evaluated at the next step).
        
Second, we will explore the collected data. In this step we will mainly analyze the news data in order to find which
news portals to consider.

Finally, we will process the data. We first estimate the risk factor process given the term structure data
(:ref:`model-term-structure`). Then we measure the volatility of the risk factor process
(:ref:`model-volatility`). After we calculate the total political news volume after the
news portals selected in the previous step, we will be able to test the causality between the news volume
and the spot rate volatility (:ref:`model-causal-relations`).
            
Preliminary Data
""""""""""""""""

Methods
^^^^^^^
    
First, we will analyze the risk of the term structure with the Vasicek model :cite:vasicek1977. The model has one state factor, therefore we can represent all the risk of the term structure with a single stochastic process. After we estimate this stochastic process, we calculate its volatility with a GARCH model :cite:{bollerslev1986. The GARCH model has conditional volatility, generating from its estimation a stochastic process of the volatility. Finally, we estimate the Granger causality :cite:{granger1969 between the political news volume process and the volatility process. The results from this estimation will answer the research problem, showing whether political events affect the term structure of interest rates.
    
.. _model-term-structure:

A Model of the Term Structure
"""""""""""""""""""""""""""""
        
In order to estimate the risk factor process we will use the :cite:`vasicek1977` model of the term structure. This is a
one factor continuous affine model, based on an arbitrage argument. Three assumptions are made:

#. the spot rate follows a diffusion process,
#. the price of a discount bond depends only on the spot rate over its term,
#. the market is efficient.

From these assumptions it follows that the spot rate is the only state variable of the term structure, and the only
source of risk. Adding two more assumptions - the market price of risk is a constant and the spot rate follows a
Ornstein-Uhlenbeck process - we arrive at a specific case of the model, which will be the one considered in this
research, and which main results are the following:
            
the spot rate follows the process
            
:math:`\mathrm{dr = \alpha(\gamma-r)\mathrm{dt + \rho \mathrm{dz`
            
and the term structure takes the form
            
:math:`R(t,T) = R(\infty) + (r(r)-R(\infty))\frac{1{\alpha T (1 - e^{-\alpha T) + \frac{\rho^2{4\alpha^3 T(1 - e^{-\alpha T)^2`
            
where
            
:math:`R(\infty) = \gamma + \frac{p\rho{\alpha - \frac{1{2 \frac{p^2{\alpha^2`

.. _model-volatility:
        
A Model of Volatility
"""""""""""""""""""""
        
We will measure the spot rate volatility with the :cite:{bollerslev1986 model, namely the Generalized Auto Regressive
Conditional Heteroskedasticity (GARCH) model. This is a parametric model, where the conditional variance is specified
as a linear function of lagged sample and conditional variances.
            
The model is given by the following equations:
            
:math:`\varepsilon_t | \psi_{t-1 ~ N(0, h_t)`
            
:math:`h_t = \alpha_0 + \sum^q_{i=1 \alpha_i \varepsilon^2_{t-i + \sum^p_{i=1 \beta_i h_{t-1`
        
.. _model-causal-relations:

A Model of Causal Relations
"""""""""""""""""""""""""""
        
Causality will be measured using the Granger model :cite:{granger1969. In this model, causality means predictive
causality: a variable causes the other if predictions made with information on the first and the latter are better
than predictions made with information only on the latter.
            