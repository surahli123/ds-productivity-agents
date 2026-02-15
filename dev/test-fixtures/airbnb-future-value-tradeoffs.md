# Source: https://medium.com/airbnb-engineering/how-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5

[Sitemap](/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

## [The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---publication_nav-53c7c27702d5-3aa99a941ba5---------------------------------------)

·

Follow publication

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:38:38/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_sidebar-53c7c27702d5-3aa99a941ba5---------------------------------------)

Creative engineers and data scientists building a world where you can belong anywhere. <http://airbnb.io>

Follow publication

Top highlight

1

# How Airbnb Measures Future Value to Standardize Tradeoffs

## The propensity score matching model powering how we optimize for long-term decision-making

[![Jenny Chen](https://miro.medium.com/v2/resize:fill:32:32/1*77Cb8d13mYUyLVrUh27NRw.jpeg)](/@djennchen?source=post_page---byline--3aa99a941ba5---------------------------------------)

[Jenny Chen](/@djennchen?source=post_page---byline--3aa99a941ba5---------------------------------------)

Follow

11 min read

·

Jul 13, 2021

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F3aa99a941ba5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&user=Jenny+Chen&userId=3fae31da9c8f&source=---header_actions--3aa99a941ba5---------------------clap_footer------------------)

601

3

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F3aa99a941ba5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&source=---header_actions--3aa99a941ba5---------------------bookmark_footer------------------)

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D3aa99a941ba5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&source=---header_actions--3aa99a941ba5---------------------post_audio_button------------------)

Share

By [Mitra Akhtari](https://www.linkedin.com/in/mitra-akhtari/), [Jenny Chen](https://www.linkedin.com/in/jennychen96/), [Amelia Lemionet](https://www.linkedin.com/in/amelialemionet), [Dan Nguyen](https://www.linkedin.com/in/dan-nguyen-b8817a34/), [Hassan Obeid](https://www.linkedin.com/in/hassan-obeid/), [Yunshan Zhu](https://www.linkedin.com/in/yunshanz/)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/0*u3P2iMzEh4mLglRq)

At Airbnb, we have a [vision](https://news.airbnb.com/brian-cheskys-open-letter-to-the-airbnb-community-about-building-a-21st-century-company/) to build a 21st century company by operating over an infinite time horizon and balancing the interests of all stakeholders. To do so effectively, we need to be able to compare, in a common currency, both the short and long-term value of actions and events that take place on our platform. These actions could be a guest making a booking or a host adding amenities to their listing, to name just two examples.

Though randomized experiments measure the initial impact of some of these actions, others, such as cancellations, are difficult to evaluate using experiments due to ethical, legal, or user experience concerns. Metrics in experiments can be hard to interpret as well, especially if the experiment affects opposing metrics (e.g., bookings increase but so do cancellations). Additionally, regardless of our ability to assess causal impact with A/B testing, [experiments are often run only for a short period of time](/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7) and do not allow us to quantify impact over an extended period.

So what did we build to solve this problem?

## **Introducing Future Incremental Value (FIV)**

We are interested in the long-term causal effect or “future incremental value” (FIV) of an action or event that occurs on Airbnb. We define “long-term” as 1 year, though our framework can adjust the time period to be as short as 30 days or as long as 2 years.

To use a concrete example, assume we would like to estimate the long-term impact of a guest making a booking. Denote the _n1_ number of users who make a booking within a month as _i ∈a1_ and the _n0_ number of users who do not make a booking in that time period as _i∈a0_. In the following year, each of these users generates revenue (or any other outcome of interest) denoted by _y_. The naive approach to computing the impact of making a booking would be to simply look at the average differences between users who made a booking versus those that did not:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*Vxqdv4sg3gdaHP5p)

However, these two groups of users are very different: those who made a booking “selected” into doing so. This selection bias obscures the true causal effect of the action, _FIV(a)_.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*EiXkA-AcIEMhDMB2)

Our goal is to exclude the bias from the naive estimate to identify _FIV(a)_.

## **The Science Behind FIV**

To minimize selection bias in estimating the FIV of an action, we need to compare observations from users or listings that are similar in every way except for whether or not they took or experienced an action. The well-documented, quasi-experimental methodology we have chosen for this problem is [propensity score matching](https://academic.oup.com/biomet/article/70/1/41/240879?login=true) (PSM). We start by separating users or listings into two groups: observations from those that took the action (“focal”) during a given timeframe and observations from those that did not (“complement”). Using PSM, we construct a “counterfactual” group, a subset of the complement that matches the characteristics of the focal as much as possible, except that these users or listings did not take the action. The assumption is that “assignment” into focal versus counterfactual is as good as random.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*F43MRwKtSDShhbRi)

 _Figure 1. Overview of methodology behind FIV_

The specific steps we take for eliminating bias from the naive method are:

  1. _Generate the Propensity Score:_ Using a set of pre-treatment or control features describing attributes of the user or listing (e.g., number of past searches), we build a binary, tree-based classifier to predict the probability that the user or listing took the action. The output here is a propensity score for each observation.
  2. _Trim for Common Support:_ We remove from the dataset any observations that have no “matching twin” in terms of propensity score. After splitting the distribution of propensity scores into buckets, we discard observations in buckets where either the focal or complement have little representation.
  3. _Match Similar Observations:_ To create the counterfactual, we use the propensity score to match each observation in the focal to a counterpart in the complement. Various [matching strategies](https://en.wikipedia.org/wiki/Nearest_neighbor_search) can be used, such as matching in bins or via nearest neighbors.
  4. _Results:_ To get the FIV, we compute the average of the outcome or target feature in the focal minus the average in the counterfactual.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*P3Og2RJ1mLeasghj)

### Evaluation

In a supervised machine learning problem, as more data becomes available and future outcomes are actualized, the model is either validated or revised. This is not the case for FIV. The steps above give us an estimate of the incremental impact of an action, but the “true” incremental impact is never revealed. In this world, how do we evaluate the success of our model?

_Common Support:_ One of the assumptions of using PSM for causal inference is “common support”.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*POao7OeMFaC3Sv5V)

where _D = 1_ denotes observations in the focal group and _X_ are the controlling features. This assumption rules out the possibility of “perfect predictability” to guarantee that observations with the same _X_ values have a positive probability of belonging to both groups and thus can be matched together to provide valid comparisons. Plotting the distribution of propensity scores for the focal and the complement group allows for a visual inspection of this assumption. Interestingly, in the case of causal inference with PSM, a high Area Under the Curve (AUC), a desirable feature for most prediction models, means that the model is able to distinguish between focal and complement observations too well, reducing our matching quality. In such cases, we assess whether those control features are confounders that affect the output metrics and eliminate them.

_Matching Evaluation:_ Observations are considered “similar” if the distributions of key features in the focal closely match the distributions of those in the counterfactual. But how close is close enough? To quantify this, we compute three metrics to assess the quality of the matching, as described in [Rubin (2001)](http://sekhon.berkeley.edu/papers/other/Rubin2001.pdf). These metrics identify whether the propensity score and key control features have similar distributions in the focal and counterfactual groups. Additionally, we are currently investigating whether to apply an additional regression adjustment to correct for any remaining imbalance in the key control features. For instance, after the matching stage, we could run a regression that directly controls for key features that we want an almost exact match for.

_Past experiments:_ Company-wide, we run experiments to test various hypotheses on how to improve the user experience, potentially leading to positive outcomes such as a significant increase in bookings. These experiments generate a source of variation in the likelihood of guests making a booking that does not suffer from selection bias, due to the randomization of treatment assignment in the experiment. By tracking and comparing the users in the control group to users in the treatment groups of these experiments, we observe the “long-term impact of making a booking”, which we can compare to our FIV estimate for “guest booking”. While the FIV estimate is a global average and experiments often estimate [local average treatment effects](https://www.aeaweb.org/articles?id=10.1257%2F000282806776157641), we can still use experimental benchmarks as an important gut check.

## **Adapting FIV for Airbnb**

While PSM is a well-established method for causal inference, we must also address several additional challenges, including the fact that Airbnb operates in a two-sided marketplace. Accordingly, the FIV platform must support computation from both the guest and the listing perspective. Guest FIV estimates the impact of actions based on activity a guest generates on Airbnb after experiencing an action, while listing FIV is from the lens of a listing. We are still in the process of developing a “host-level” FIV. One challenge in doing so will be sample size: we have fewer unique hosts than listings.

## Get Jenny Chen’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

To arrive at a “platform” or total FIV for an action, we cannot simply add guest and listing FIVs together because of double counting. We simplify the problem and only count the value from the guest-side or the listing-side depending on which mechanisms we believe drive the majority of the long-term impact.

Another feature of our two-sided market is cannibalization, especially on the supply-side: if a listing gets more bookings, some portion of this increase is taking away bookings from similar listings. In order to arrive at the true “incremental” value of an action, we apply cannibalization haircuts to listing FIV estimates based on our understanding of the magnitude of this cannibalization from experimental data.

## **The Platform Powering FIV**

FIV is a data product and its clients are other teams within Airbnb. We provide an easy to use platform to organize, compute, and analyze actions and FIVs at scale. As part of this, we have built components that take in input from the client, construct and store necessary data, productionize the PSM model, compute FIVs, and output the results. The machinery, orchestrated through [Airflow](https://airflow.apache.org/docs/apache-airflow/2.0.1/) and invisible to the client, looks as follows:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*IqZbWBgn0wJFgXGd)

 _Figure 2. Overview of FIV Platform_

### Client Input

Use cases begin with a conversation with the client team to understand the business context and technical components of their desired estimate. An integral part of producing valid and useful FIV estimates is establishing well-defined focal and complement groups. Additionally, there are cases when the FIV tools are not applicable, such as when there is limited observational data (e.g., a new feature) or small group sizes (e.g., a specific funnel or lever).

The client submits a configuration file defining their focal and complement groups, which is essentially the only task the client does in order to use the FIV platform. Below is the config for the FIV of “guest booking”: a visitor who booked a home on our site (focal) versus one who did not book a home (complement).

Figure 3. Example of an FIV config that would be submitted by a client

The _cohort_ identifies the maximum set of users to consider (in this case, all visitors to Airbnb’s platform), some of which are removed from consideration by the _filter_query_ (in this case, users who also booked an Airbnb experience are removed). From the remaining set of users, the _action_event_query_ allocates users to the focal with leftovers automatically assigned to the complement.

After the client’s config is reviewed, it is merged into the FIV repository and automatically ingested into our pipelines. We assign a version to each unique config to allow for iteration while storing historical results.

We have designed the platform to be as easy to use as possible. No special knowledge of modeling, inference, or complex coding is needed. The client only needs to provide a set of queries to define their groups and we take care of the rest!

### Data Pipeline

The config triggers a pipeline to construct the focal and complement, join them with control and target features, and store this in the Data Warehouse. Control features will later serve as inputs into the propensity score model, whereas target features will be the outcomes that FIV is computed over. Target features are what allow us to convert actions from different contexts and parts of Airbnb into a “common currency”. This is one of FIV’s superpowers!

Leveraging [Zipline](https://databricks.com/session/zipline-airbnbs-machine-learning-data-management-platform) as our feature management system, we currently have approximately 1,000 control features across both guests and listings, such as region, cancellations, or past searches. Though we have the capability to compute FIV in terms of numerous target features, we have a few target features that give us a standardized output, such as revenue, cost, and bookings.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*keT6ycZkmSs4an8L)

 _Figure 4. Steps to compute the raw data needed for FIV, after taking in client input_

The version of the config is also used here to automate backfills, significantly decreasing manual errors and intervention. There are multiple checks on the versioning to ensure that the data produced is always aligned with the latest config.

### Modeling Pipeline

Because the focal and complement groups can be very large and costly to use in modeling, we downsample and use a subset of our total observations. To account for sampling noise, we take multiple samples from the output of our data pipeline and feed each sampling round into our modeling pipeline. Sampling improves our SLA, ensures each group has the same cardinality and allows us to get a sense of sampling noise. Outliers are also removed to limit the noisiness of our estimates.

The PSM model is built on top of [Bighead](https://ieeexplore.ieee.org/document/8964147), Airbnb’s machine learning platform. After fetching the sampled data, we perform feature selection, clean the features, and run PSM to produce FIVs in terms of each target feature before finally writing our results into the Data Warehouse. In addition to the FIVs themselves, we also collect and store evaluation metrics as well as metrics such as feature importance and runtime.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*Hm6aj1TSpXLjd5kU)

 _Figure 5. Modeling steps needed to compute FIV, after the raw data has been generated_

On top of the modeling pipeline we have built the ability to prioritize actions and rate limit the number of tasks we launch, giving us a big picture view of the resources being used.

### FIVs!

Next we pull our FIVs into a [Superset](/airbnb-engineering/supercharging-apache-superset-b1a2393278bd) dashboard for easy access by our clients. FIV point estimates and confidence intervals (estimated by [bootstrapping](https://ocw.mit.edu/courses/mathematics/18-05-introduction-to-probability-and-statistics-spring-2014/readings/MIT18_05S14_Reading24.pdf)) are based on the last 6 months of available data to smooth over seasonality or month-level fluctuations. We distinguish between the value generated by the action itself (tagged as “Present” below) and the residual downstream value (“Future”) of the action.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*wM0yfjWPOP1NU9Yb)

 _Figure 6. Snapshot of the dashboard as seen by clients_

## **FIV as a Product**

Airbnb’s two-sided marketplace creates interesting but complicated tradeoffs. To quantify these tradeoffs in a common currency, especially when experimentation is not possible, we have built the FIV framework. This has allowed teams to make standardized, data-informed prioritization decisions that account for both immediate _and_ long-term payoffs.

Currently, we have scaled to work with _all_ teams from across the company (demand-side, supply-side, platform teams like Payments and Customer Support, and even the company’s most recent team, [Airbnb.org](https://www.airbnb.org/)) and computed over 150 FIV action events from the guest and listing perspective. Use cases range from return on investment calculations (what is the monetary value of a “perfect” stay?) to determining the long-term value of guest outreach emails that may not always generate immediate output metrics. We have also used FIV to inform the [overall evaluation criteria](https://www.linkedin.com/pulse/overall-evaluation-criterion-oec-ronny-kohavi/) in [experiments](/airbnb-engineering/designing-experimentation-guardrails-ed6a976ec669) (what weights do we use when trading off increased bookings and cancellations?) and rank different listing levers to understand what to prioritize (what features or amenities are most useful for a host to adopt?).

In the absence of a centralized, scalable FIV platform, each individual team would need to create their own framework, methodology, and pipelines to assess and trade off long-term value, which would be inefficient and leave room for errors and inconsistencies. We have boiled down this complex problem into essentially writing two queries with everything else done behind the scenes by our machinery.

Yet, our work is not done–we plan to continue improving the workflow experience and explore new models in order to improve our estimates. The future of FIV at Airbnb is bright!

## **Acknowledgments**

FIV has been an effort spanning multiple teams and years. We’d like to especially thank [Diana Chen](https://www.linkedin.com/in/diana-chen-42332939/) and [Yuhe Xu](https://www.linkedin.com/in/xuyuhe/) for contributing to the development of FIV and the teams who have onboarded and placed trust into FIV.

[Data Science](/tag/data-science?source=post_page-----3aa99a941ba5---------------------------------------)

[Data Platforms](/tag/data-platforms?source=post_page-----3aa99a941ba5---------------------------------------)

[Experimentation](/tag/experimentation?source=post_page-----3aa99a941ba5---------------------------------------)

[Data](/tag/data?source=post_page-----3aa99a941ba5---------------------------------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F3aa99a941ba5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&user=Jenny+Chen&userId=3fae31da9c8f&source=---footer_actions--3aa99a941ba5---------------------clap_footer------------------)

601

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F3aa99a941ba5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&user=Jenny+Chen&userId=3fae31da9c8f&source=---footer_actions--3aa99a941ba5---------------------clap_footer------------------)

601

3

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F3aa99a941ba5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&source=---footer_actions--3aa99a941ba5---------------------bookmark_footer------------------)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:48:48/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--3aa99a941ba5---------------------------------------)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:64:64/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--3aa99a941ba5---------------------------------------)

Follow

## [Published in The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--3aa99a941ba5---------------------------------------)

[156K followers](/airbnb-engineering/followers?source=post_page---post_publication_info--3aa99a941ba5---------------------------------------)

·[Last published 4 days ago](/airbnb-engineering/my-journey-to-airbnb-anna-sulkina-85216183d094?source=post_page---post_publication_info--3aa99a941ba5---------------------------------------)

Creative engineers and data scientists building a world where you can belong anywhere. <http://airbnb.io>

Follow

[![Jenny Chen](https://miro.medium.com/v2/resize:fill:48:48/1*77Cb8d13mYUyLVrUh27NRw.jpeg)](/@djennchen?source=post_page---post_author_info--3aa99a941ba5---------------------------------------)

[![Jenny Chen](https://miro.medium.com/v2/resize:fill:64:64/1*77Cb8d13mYUyLVrUh27NRw.jpeg)](/@djennchen?source=post_page---post_author_info--3aa99a941ba5---------------------------------------)

Follow

## [Written by Jenny Chen](/@djennchen?source=post_page---post_author_info--3aa99a941ba5---------------------------------------)

[70 followers](/@djennchen/followers?source=post_page---post_author_info--3aa99a941ba5---------------------------------------)

·[2 following](/@djennchen/following?source=post_page---post_author_info--3aa99a941ba5---------------------------------------)

Follow

## Responses (3)

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--3aa99a941ba5---------------------------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-future-value-to-standardize-tradeoffs-3aa99a941ba5&source=---post_responses--3aa99a941ba5---------------------respond_sidebar------------------)

Cancel

Respond

[![Vinit Shah](https://miro.medium.com/v2/resize:fill:32:32/0*9I0sAaHQAslH6mfh.)](/@vinitshah_61782?source=post_page---post_responses--3aa99a941ba5----0-----------------------------------)

[Vinit Shah](/@vinitshah_61782?source=post_page---post_responses--3aa99a941ba5----0-----------------------------------)

[Apr 23, 2022](/@vinitshah_61782/wouldnt-each-action-event-possibly-have-a-different-set-of-confounders-fe45aeab6245?source=post_page---post_responses--3aa99a941ba5----0-----------------------------------)
    
    
    Wouldn't each action event possibly have a different set of confounders? How does FIV deal with this at scale?

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2Ffe45aeab6245&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40vinitshah_61782%2Fwouldnt-each-action-event-possibly-have-a-different-set-of-confounders-fe45aeab6245&user=Vinit+Shah&userId=340a2d016529&source=---post_responses--fe45aeab6245----0-----------------respond_sidebar------------------)

Reply

[![James Liao](https://miro.medium.com/v2/resize:fill:32:32/0*zu1wuBF_Yl0EDM5Y.)](/@ressonliao?source=post_page---post_responses--3aa99a941ba5----1-----------------------------------)

[James Liao](/@ressonliao?source=post_page---post_responses--3aa99a941ba5----1-----------------------------------)

[Aug 12, 2021](/@ressonliao/excellent-post-good-way-to-evaluate-functions-f693cf0fdec0?source=post_page---post_responses--3aa99a941ba5----1-----------------------------------)
    
    
    excellent post, good way to evaluate functions!

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2Ff693cf0fdec0&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40ressonliao%2Fexcellent-post-good-way-to-evaluate-functions-f693cf0fdec0&user=James+Liao&userId=2dd9eb5c6f26&source=---post_responses--f693cf0fdec0----1-----------------respond_sidebar------------------)

Reply

[![Travis](https://miro.medium.com/v2/resize:fill:32:32/0*3-t5tHRhW-U-vthB.)](/@shiqing.sun95?source=post_page---post_responses--3aa99a941ba5----2-----------------------------------)

[Travis](/@shiqing.sun95?source=post_page---post_responses--3aa99a941ba5----2-----------------------------------)

[Jul 13, 2021 (edited)](/@shiqing.sun95/why-it-is-auc-instead-of-prauc-338410130dfc?source=post_page---post_responses--3aa99a941ba5----2-----------------------------------)

a high Area Under the Curve (AUC),
    
    
    Why it is AUC instead of PRAUC? I think sometimes we need to focus on subpopulation with high propensity score instead all of the population. Thus, our model should perform well on subpopulation with high propensity score, which means it should has a good PRAUC.

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F338410130dfc&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40shiqing.sun95%2Fwhy-it-is-auc-instead-of-prauc-338410130dfc&user=Travis&userId=d61078b42e27&source=---post_responses--338410130dfc----2-----------------respond_sidebar------------------)

Reply

## More from Jenny Chen and The Airbnb Tech Blog

![A Deep Dive into Airbnb’s Server-Driven UI System](https://miro.medium.com/v2/resize:fit:679/format:webp/0*CedYKpSYMIGEiX7m)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----0---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----0---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

by

[Ryan Brooks](/@rbro112?source=post_page---author_recirc--3aa99a941ba5----0---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

## [A Deep Dive into Airbnb’s Server-Driven UI SystemHow Airbnb ships features faster across web, iOS, and Android using a server-driven UI system named Ghost Platform 👻.](/airbnb-engineering/a-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5?source=post_page---author_recirc--3aa99a941ba5----0---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

Jun 29, 2021

[A clap icon4.3KA response icon40](/airbnb-engineering/a-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5?source=post_page---author_recirc--3aa99a941ba5----0---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F842244c5f5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fa-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5&source=---author_recirc--3aa99a941ba5----0-----------------bookmark_preview----254356cd_ab09_4245_9772_c96d040875b8--------------)

![Pay As a Local](https://miro.medium.com/v2/resize:fit:679/format:webp/1*6K6D4WxFwqlwdtBc6uzczw.jpeg)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----1---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----1---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

by

[Gerum Haile](/@gerum.haile?source=post_page---author_recirc--3aa99a941ba5----1---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

## [Pay As a LocalHow Airbnb rolled out 20+ locally relevant payment methods worldwide in just 14 months](/airbnb-engineering/pay-as-a-local-bef469b72f32?source=post_page---author_recirc--3aa99a941ba5----1---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

Jan 12

[A clap icon82A response icon1](/airbnb-engineering/pay-as-a-local-bef469b72f32?source=post_page---author_recirc--3aa99a941ba5----1---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fbef469b72f32&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fpay-as-a-local-bef469b72f32&source=---author_recirc--3aa99a941ba5----1-----------------bookmark_preview----254356cd_ab09_4245_9772_c96d040875b8--------------)

![How Airbnb Achieved Metric Consistency at Scale](https://miro.medium.com/v2/resize:fit:679/format:webp/1*rB53PQsJi73IeA-eIeucIg.png)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----2---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----2---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

by

[Robert Chang](/@rchang?source=post_page---author_recirc--3aa99a941ba5----2---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

## [How Airbnb Achieved Metric Consistency at ScalePart-I: Introducing Minerva — Airbnb’s Metric Platform](/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70?source=post_page---author_recirc--3aa99a941ba5----2---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

Apr 30, 2021

[A clap icon2.2KA response icon10](/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70?source=post_page---author_recirc--3aa99a941ba5----2---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff23cc53dea70&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70&source=---author_recirc--3aa99a941ba5----2-----------------bookmark_preview----254356cd_ab09_4245_9772_c96d040875b8--------------)

![Dynamic Kubernetes Cluster Scaling at Airbnb](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Elojmgc7Y06tItOaLdB0Cw.jpeg)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----3---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5----3---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

by

[David Morrison](/@drmorr-airbnb?source=post_page---author_recirc--3aa99a941ba5----3---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

## [Dynamic Kubernetes Cluster Scaling at AirbnbAuthors: Evan Sheng, David Morrison](/airbnb-engineering/dynamic-kubernetes-cluster-scaling-at-airbnb-d79ae3afa132?source=post_page---author_recirc--3aa99a941ba5----3---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

May 23, 2022

[A clap icon550A response icon1](/airbnb-engineering/dynamic-kubernetes-cluster-scaling-at-airbnb-d79ae3afa132?source=post_page---author_recirc--3aa99a941ba5----3---------------------254356cd_ab09_4245_9772_c96d040875b8--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fd79ae3afa132&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdynamic-kubernetes-cluster-scaling-at-airbnb-d79ae3afa132&source=---author_recirc--3aa99a941ba5----3-----------------bookmark_preview----254356cd_ab09_4245_9772_c96d040875b8--------------)

[See all from Jenny Chen](/@djennchen?source=post_page---author_recirc--3aa99a941ba5---------------------------------------)

[See all from The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--3aa99a941ba5---------------------------------------)

## Recommended from Medium

![Data Engineering Design Patterns You Must Learn in 2026](https://miro.medium.com/v2/resize:fit:679/format:webp/1*0cuVBpD9ZUDcnV3U1mV8cg.png)

[![AWS in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*6EeD87OMwKk-u3ncwAOhog.png)](https://medium.com/aws-in-plain-english?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

In

[AWS in Plain English](https://medium.com/aws-in-plain-english?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

by

[Khushbu Shah](/@khushbu.shah_661?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

## [Data Engineering Design Patterns You Must Learn in 2026These are the 8 data engineering design patterns every modern data stack is built on. Learn them once, and every data engineering tool…](/aws-in-plain-english/data-engineering-design-patterns-you-must-learn-in-2026-c25b7bd0b9a7?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

Jan 5

[A clap icon907A response icon19](/aws-in-plain-english/data-engineering-design-patterns-you-must-learn-in-2026-c25b7bd0b9a7?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fc25b7bd0b9a7&operation=register&redirect=https%3A%2F%2Faws.plainenglish.io%2Fdata-engineering-design-patterns-you-must-learn-in-2026-c25b7bd0b9a7&source=---read_next_recirc--3aa99a941ba5----0-----------------bookmark_preview----5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

![6 brain images](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Q-mzQNzJSVYkVGgsmHVjfw.png)

[![Write A Catalyst](https://miro.medium.com/v2/resize:fill:20:20/1*KCHN5TM3Ga2PqZHA4hNbaw.png)](https://medium.com/write-a-catalyst?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

In

[Write A Catalyst](https://medium.com/write-a-catalyst?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

by

[Dr. Patricia Schmidt](/@creatorschmidt?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

## [As a Neuroscientist, I Quit These 5 Morning Habits That Destroy Your BrainMost people do #1 within 10 minutes of waking (and it sabotages your entire day)](/write-a-catalyst/as-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

Jan 14

[A clap icon29KA response icon500](/write-a-catalyst/as-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F3efe1f410226&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fwrite-a-catalyst%2Fas-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226&source=---read_next_recirc--3aa99a941ba5----1-----------------bookmark_preview----5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

![I Stopped Using ChatGPT for 30 Days. What Happened to My Brain Was Terrifying.](https://miro.medium.com/v2/resize:fit:679/format:webp/1*z4UOJs0b33M4UJXq5MXkww.png)

[![Level Up Coding](https://miro.medium.com/v2/resize:fill:20:20/1*5D9oYBd58pyjMkV_5-zXXQ.jpeg)](https://medium.com/gitconnected?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

In

[Level Up Coding](https://medium.com/gitconnected?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

by

[Teja Kusireddy](/@teja.kusireddy23?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

## [I Stopped Using ChatGPT for 30 Days. What Happened to My Brain Was Terrifying.91% of you will abandon 2026 resolutions by January 10th. Here’s how to be in the 9% who actually win.](/gitconnected/i-stopped-using-chatgpt-for-30-days-what-happened-to-my-brain-was-terrifying-70d2a62246c0?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

Dec 28, 2025

[A clap icon5.5KA response icon220](/gitconnected/i-stopped-using-chatgpt-for-30-days-what-happened-to-my-brain-was-terrifying-70d2a62246c0?source=post_page---read_next_recirc--3aa99a941ba5----0---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F70d2a62246c0&operation=register&redirect=https%3A%2F%2Flevelup.gitconnected.com%2Fi-stopped-using-chatgpt-for-30-days-what-happened-to-my-brain-was-terrifying-70d2a62246c0&source=---read_next_recirc--3aa99a941ba5----0-----------------bookmark_preview----5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

![Stop Memorizing Design Patterns: Use This Decision Tree Instead](https://miro.medium.com/v2/resize:fit:679/format:webp/1*xfboC-sVIT2hzWkgQZT_7w.png)

[![Women in Technology](https://miro.medium.com/v2/resize:fill:20:20/1*kd0DvPkLdn59Emtg_rnsqg.png)](https://medium.com/womenintechnology?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

In

[Women in Technology](https://medium.com/womenintechnology?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

by

[Alina Kovtun✨](/@akovtun?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

## [Stop Memorizing Design Patterns: Use This Decision Tree InsteadChoose design patterns based on pain points: apply the right pattern with minimal over-engineering in any OO language.](/womenintechnology/stop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

Jan 29

[A clap icon3.1KA response icon26](/womenintechnology/stop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa?source=post_page---read_next_recirc--3aa99a941ba5----1---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fe84f22fca9fa&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fwomenintechnology%2Fstop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa&source=---read_next_recirc--3aa99a941ba5----1-----------------bookmark_preview----5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

![Stanford Just Killed Prompt Engineering With 8 Words \(And I Can’t Believe It Worked\)](https://miro.medium.com/v2/resize:fit:679/format:webp/1*va3sFwIm26snbj5ly9ZsgA.jpeg)

[![Generative AI](https://miro.medium.com/v2/resize:fill:20:20/1*M4RBhIRaSSZB7lXfrGlatA.png)](https://medium.com/generative-ai?source=post_page---read_next_recirc--3aa99a941ba5----2---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

In

[Generative AI](https://medium.com/generative-ai?source=post_page---read_next_recirc--3aa99a941ba5----2---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

by

[Adham Khaled](/@adham__khaled__?source=post_page---read_next_recirc--3aa99a941ba5----2---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

## [Stanford Just Killed Prompt Engineering With 8 Words (And I Can’t Believe It Worked)ChatGPT keeps giving you the same boring response? This new technique unlocks 2× more creativity from ANY AI model — no training required…](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--3aa99a941ba5----2---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

Oct 19, 2025

[A clap icon23KA response icon618](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--3aa99a941ba5----2---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F8349d6524d2b&operation=register&redirect=https%3A%2F%2Fgenerativeai.pub%2Fstanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b&source=---read_next_recirc--3aa99a941ba5----2-----------------bookmark_preview----5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

![An example of a perfect, human designed dashboard interface for desktop and mobile phone](https://miro.medium.com/v2/resize:fit:679/format:webp/1*C8RVDKs_uZrVUdgpsF6Fmw.png)

[![Michal Malewicz](https://miro.medium.com/v2/resize:fill:20:20/1*149zXrb2FXvS_mctL4NKSg.png)](/@michalmalewicz?source=post_page---read_next_recirc--3aa99a941ba5----3---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[Michal Malewicz](/@michalmalewicz?source=post_page---read_next_recirc--3aa99a941ba5----3---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

## [The End of Dashboards and Design SystemsDesign is becoming quietly human again.](/@michalmalewicz/the-end-of-dashboards-and-design-systems-5d98ec9de627?source=post_page---read_next_recirc--3aa99a941ba5----3---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

Nov 26, 2025

[A clap icon5.6KA response icon212](/@michalmalewicz/the-end-of-dashboards-and-design-systems-5d98ec9de627?source=post_page---read_next_recirc--3aa99a941ba5----3---------------------5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F5d98ec9de627&operation=register&redirect=https%3A%2F%2Fmichalmalewicz.medium.com%2Fthe-end-of-dashboards-and-design-systems-5d98ec9de627&source=---read_next_recirc--3aa99a941ba5----3-----------------bookmark_preview----5733dd2c_427b_45a7_9187_bfd86fe8f921--------------)

[See more recommendations](/?source=post_page---read_next_recirc--3aa99a941ba5---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----3aa99a941ba5---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----3aa99a941ba5---------------------------------------)

[About](/about?autoplay=1&source=post_page-----3aa99a941ba5---------------------------------------)

[Careers](/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----3aa99a941ba5---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----3aa99a941ba5---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----3aa99a941ba5---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----3aa99a941ba5---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----3aa99a941ba5---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----3aa99a941ba5---------------------------------------)