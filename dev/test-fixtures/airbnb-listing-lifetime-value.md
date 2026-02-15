# Source: https://medium.com/airbnb-engineering/how-airbnb-measures-listing-lifetime-value-a603bf05142c

[Sitemap](/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

## [The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---publication_nav-53c7c27702d5-a603bf05142c---------------------------------------)

·

Follow publication

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:38:38/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_sidebar-53c7c27702d5-a603bf05142c---------------------------------------)

Creative engineers and data scientists building a world where you can belong anywhere. <http://airbnb.io>

Follow publication

# **How Airbnb Measures Listing Lifetime Value**

[![Carlos Sanchez Martinez](https://miro.medium.com/v2/resize:fill:32:32/1*X9z6qvBRm1Xlu4rF9XjMTw.jpeg)](/@carlos.sanchezmartinez?source=post_page---byline--a603bf05142c---------------------------------------)

[Carlos Sanchez Martinez](/@carlos.sanchezmartinez?source=post_page---byline--a603bf05142c---------------------------------------)

Follow

8 min read

·

Mar 26, 2025

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2Fa603bf05142c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&user=Carlos+Sanchez+Martinez&userId=deed279ada7f&source=---header_actions--a603bf05142c---------------------clap_footer------------------)

122

3

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fa603bf05142c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&source=---header_actions--a603bf05142c---------------------bookmark_footer------------------)

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Da603bf05142c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&source=---header_actions--a603bf05142c---------------------post_audio_button------------------)

Share

A deep dive on the framework that lets us identify the most valuable listings for our guests.

**By:** [Carlos Sanchez-Martinez](https://www.linkedin.com/in/carlossanchezmartinez/), [Sean O’Donnell](https://www.linkedin.com/in/seanmk2/), [Lo-Hua Yuan](https://www.linkedin.com/in/lohua-yuan/), [Yunshan Zhu](https://www.linkedin.com/in/yunshanz/)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*JSoY6CDkTMQEFXgP)

At Airbnb, we always strive to provide our community with the best experience. To do so, it’s important to understand what kinds of accommodation listings are valuable to our guests. We achieve this by calculating and using estimates of **listing lifetime value**. These estimates not only allow us to identify which types of listings resonate best with guests, but also help us develop resources and recommendations for hosts to increase the value driven by their listings.

Most of the existing literature on lifetime value focuses on traditional sales channels in which a single seller transacts with many buyers (e.g. a retailer selling clothing to a customer). In contrast, this blog post explains how we model lifetime value in a platform like Airbnb, with multiple sellers and buyers. In the first section, we describe our general listings lifetime value framework. In the second section, we discuss relevant challenges when putting this framework into practice.

## Our Listing Lifetime Value Framework

Our listing lifetime value (LTV) framework estimates three different quantities of interest: baseline LTV, incremental LTV, and marketing-induced incremental LTV.

### (1) Baseline LTV

To measure LTV, we need to define what we mean by “value” and what time horizon constitutes a “lifetime.” Simplifying slightly for the purposes of this blog post, we define and estimate our baseline listing LTV as the total number of bookings that a listing will make on Airbnb over the next 365 days.

We rely on machine learning and the rich information we have about our listings to estimate this quantity for each individual listing. In practice, we also follow financial guidance to arrive at present value by projecting outcomes into the future and applying a relevant discount rate to future value.

Table 1 shows some hypothetical baseline LTV estimates. As you can see from the examples, LTV is not static, and can evolve as we improve the accuracy of our estimates, observe changes in our marketplace, or even develop a listing (e.g., by providing guidance that helps hosts improve the listing to get more bookings).

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*PLgiegXaNpY8nthDFZpmpA.png)

**Table 1. Example Listing LTV Estimates**

We use baseline LTV estimates to segment our listings and identify which types of listings resonate best with our guests. This informs our supply expansion strategy. We also use baseline LTV to identify listings that are not expected to reach their full booking potential and may benefit from additional guidance.

### (2) Incremental LTV

When estimating lifetime value, we face a challenge that is common across multi-sided marketplaces: the transactions made by one listing might come at the expense of another listing’s transactions. For example, when a new listing joins our marketplace, this listing will get some bookings from guests who were previously booking other listings. We need to account for this dynamic if we want to accurately measure how much value is _added_ by each listing.

We address this challenge by creating “incremental __ LTV” estimates. We refer to the additional transactions that would not have occurred without the listing’s participation as “incremental value,” and the transactions that would have occurred even without the listing’s participation as “cannibalized value.” We estimate the incremental LTV for a listing by subtracting cannibalized value estimates from the baseline LTV. We explain this adjustment in more detail when discussing measurement challenges.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*UH0hKFiaFYB-l_LL-CkSRQ.png)

**Figure 1. Cannibalization.** In this context, cannibalization refers to the transactions that would have occurred even without a listing’s participation in the marketplace. For example, when a new listing joins the platform, some bookings obtained by that listing would have been made at other listings on the platform had the new listing not joined.

### (3) Marketing-induced incremental LTV

Lifetime value is not static, and our LTV model needs to tell us how our internal initiatives bring additional listing value. For example, suppose we run a marketing campaign that provides hosts with tips on how to successfully improve their listings. To understand the return from the campaign, we need to measure how much value is accrued due to the campaign, and how much value would have been organically accrued without our marketing intervention. We calculate “marketing-induced incremental LTV” to measure how much additional listing LTV is created by our internal initiatives.

Having outlined our measurement framework (summarized in Figure 2), we now cover some of the technical challenges we faced when putting this framework into practice.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*RIUqYmgP_5JWfAohtdCdBQ.png)

**Figure 2.** **Listing LTV Framework**

## Challenges when measuring Listing Lifetime Value

### Challenge (1): Accurately measuring baseline LTV

The most important requirement for our framework is accurate estimation of baseline LTV. Figure 3 illustrates our estimation setup. First, we leverage listing features snapshotted at estimation time t. This data includes rich knowledge we have about each listing and host (availability, price, location, host tenure, etc). We then use these features to train our machine learning model. As a value label, we use the number of bookings made within the next 365-day period, which is observed on date t + 365.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*6EanAK-Y42jbcWyATva8GA.png)

**Figure 3. Label vs. Feature Collection.** Our label lands 365 days after we collect the initial set of features for our model.

This setup has two important implications that impact accuracy and evaluation:

  * We have to wait 365 days to fully evaluate the accuracy of a prediction.
  * Our initial training data might not allow us to make accurate predictions if we observe shocks between the time when the training data was captured, and the time when we score the model.

In practice, we felt the full consequences of these implications during the COVID-19 pandemic, when travel came to a halt and marketplace dynamics changed drastically. Our model’s training data from before the pandemic had dramatically different characteristics relative to the scoring data we collected after the pandemic. When dealing with this shock, we implemented various strategies that helped us improve model accuracy:

  * Reducing training windows, allowing us to reduce model drift.
  * Feeding the model with granular geographic data and human-provided information about external factors as borders closed and reopened due to the pandemic.
  * Adopting [LightGBM](http://lightgbm.readthedocs.io), which handles high cardinality features like the geographic variables mentioned previously.

### Challenge (2): Measuring incrementality

Accounting for incrementality is challenging because we never observe the ground truth. While we observe how many bookings are made per listing, we cannot tell which bookings are incremental and which bookings are cannibalized from other listings.

## Get Carlos Sanchez Martinez’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Since we don’t have an incrementality label to estimate this outcome directly, we instead estimate a production function. Intuitively, incrementality is heavily dependent on our ability to connect both sides of our marketplace. Production functions allow us to identify when our supply of listings and demand from guests connect and provide incremental value. Incrementality estimates will be high when a segment has high guest demand and relatively low listing supply. In contrast, incrementality will be low when segments have a large volume of listing supply and relatively low demand, meaning guests have an easy time finding a place to stay and a new listing is more likely to cannibalize bookings from other listings.

Specifically, we model how our total supply of listings (S) and total demand from guests (D) impacts our target outcome bookings (O), as in equation (1):

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*ccUD00N5xq2IfTiMkZHNGA.png)

We estimate this model with historical supply, demand, and outcome data aggregated across internally-defined segments that have little overlapping demand. Having estimated model (1), we calculate how extra supply of listings results in additional bookings in the given segment: this is our estimate of incrementality.

### Challenge (3): Handling uncertainty

To handle the uncertainty we experienced during the pandemic, we began updating our LTV estimates as listings received greater or fewer numbers of bookings than initially expected. This approach has helped us capture any shocks that occur after making our initial predictions.

To show how this can be useful, let’s go back to our marketing campaign example. Assume that we run this campaign for six months, and that we measure the success of this campaign by comparing marketing-induced incremental LTV against our total marketing investment in the campaign. As a first approach, we could use the initial baseline LTV figures (which feed into marketing-induced LTV) estimated at the time when the listing was first targeted by our initiative. However, listings targeted on day 1 of the marketing campaign will have six months of booking history by the time the campaign ends and we evaluate success. A more accurate approach uses realized bookings after the initial prediction to start correcting for model error.

Table 2 illustrates how this works. Suppose that on 2024–01–01, we expect that Listing A will get a total of 16 bookings by the end of the year. If six months into the 365 day period, Listing A has received 16 bookings, we should adjust its expected value upward to, say, 21 bookings. In fact, every day for 365 days after 2024–01–01, we can look at the bookings that Listing A has accrued and adjust the expected bookings accordingly. By construction, the expected and accrued bookings converge to the final bookings 365 days after the initial booking date. Going back to our marketing example, if Listing A ultimately receives 20 bookings, updating the initial estimate means we went from 20% underprediction on day 0 to a more reasonable 5% overprediction as of month 6.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*vNQ0046lY7rfWrHIJK6Oww.png)

**Table 2.** **Example of how we update listing lifetime value estimates.**

In practice, we make daily adjustments to a listing’s expected value based on the listing’s accrued value, updated listing features, and value arrival patterns for similar listings estimated using historical data.

## Conclusion

In this blog post, we explained how we approach listing lifetime value at Airbnb. We covered our measurement framework, including baseline LTV, incremental LTV, and marketing-induced incremental LTV. We also zoomed into measurement challenges, like when travel patterns changed drastically during the COVID pandemic and accurately estimating LTV became more difficult.

Estimating the lifetime value for each listing is important because it helps us serve our community more effectively. Use cases include:

  * Identifying unique listing segments through which new hosts can showcase their hospitality to a large guest audience.
  * Pinpointing locations where listings have an opportunity to get more bookings, and might benefit from additional demand.
  * Identifying which internal marketing initiatives bring the most value to our community.

It’s also worth noting that our measurement framework may extend to other applications, such as the lifetime value for Airbnb Experiences listings, where the value of an experience listing will heavily depend on travel trends and on guests’ ability to discover these experiences.

We continue to solve interesting problems around LTV every day (and as more insights come up, we’ll keep sharing them on our blog). Can you see yourself making an impact here? If so, we encourage you to explore the [open roles on our team](https://careers.airbnb.com/positions/?_departments=data-science).

## Acknowledgments

Finally, we need to give special thanks to Airfam and alumni Sam Barrows, Robert Chang, Linsha Chen, Richard Dear, Andrey Fradkin, Ruben Lobel, Brian De Luna, Dan T. Nguyen, Vaughn Quoss, Jason Ting, and Peng Ye. Without their foundational work, these LTV models would not have been possible.

Thanks as well to Rebecca Ajuonuma, Carolina Barcenas, Nathan Brixius, Jenny Chen, Peter Coles, Lauren Mackevich, Dan Schmierer, Yvonne Wang, Shanni Weilert, and Jane Zhang for their valuable feedback when writing this blog post.

[Machine Learning](/tag/machine-learning?source=post_page-----a603bf05142c---------------------------------------)

[Lifetime Value](/tag/lifetime-value?source=post_page-----a603bf05142c---------------------------------------)

[Data Science](/tag/data-science?source=post_page-----a603bf05142c---------------------------------------)

[Engineering](/tag/engineering?source=post_page-----a603bf05142c---------------------------------------)

[AI](/tag/ai?source=post_page-----a603bf05142c---------------------------------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2Fa603bf05142c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&user=Carlos+Sanchez+Martinez&userId=deed279ada7f&source=---footer_actions--a603bf05142c---------------------clap_footer------------------)

122

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2Fa603bf05142c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&user=Carlos+Sanchez+Martinez&userId=deed279ada7f&source=---footer_actions--a603bf05142c---------------------clap_footer------------------)

122

3

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fa603bf05142c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&source=---footer_actions--a603bf05142c---------------------bookmark_footer------------------)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:48:48/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--a603bf05142c---------------------------------------)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:64:64/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--a603bf05142c---------------------------------------)

Follow

## [Published in The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--a603bf05142c---------------------------------------)

[156K followers](/airbnb-engineering/followers?source=post_page---post_publication_info--a603bf05142c---------------------------------------)

·[Last published 4 days ago](/airbnb-engineering/my-journey-to-airbnb-anna-sulkina-85216183d094?source=post_page---post_publication_info--a603bf05142c---------------------------------------)

Creative engineers and data scientists building a world where you can belong anywhere. <http://airbnb.io>

Follow

[![Carlos Sanchez Martinez](https://miro.medium.com/v2/resize:fill:48:48/1*X9z6qvBRm1Xlu4rF9XjMTw.jpeg)](/@carlos.sanchezmartinez?source=post_page---post_author_info--a603bf05142c---------------------------------------)

[![Carlos Sanchez Martinez](https://miro.medium.com/v2/resize:fill:64:64/1*X9z6qvBRm1Xlu4rF9XjMTw.jpeg)](/@carlos.sanchezmartinez?source=post_page---post_author_info--a603bf05142c---------------------------------------)

Follow

## [Written by Carlos Sanchez Martinez](/@carlos.sanchezmartinez?source=post_page---post_author_info--a603bf05142c---------------------------------------)

[47 followers](/@carlos.sanchezmartinez/followers?source=post_page---post_author_info--a603bf05142c---------------------------------------)

·[1 following](/@carlos.sanchezmartinez/following?source=post_page---post_author_info--a603bf05142c---------------------------------------)

I am a Staff Data Scientist at Airbnb. I work on recommendation engines, host success, and marketplace (supply/demand) dynamics. Stanford + UBC grad.

Follow

## Responses (3)

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--a603bf05142c---------------------------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-measures-listing-lifetime-value-a603bf05142c&source=---post_responses--a603bf05142c---------------------respond_sidebar------------------)

Cancel

Respond

[![Sophia Chen, PhD](https://miro.medium.com/v2/resize:fill:32:32/1*KiW7GjJeZcUa44YLq6SSbA.jpeg)](/@sophiachen2012?source=post_page---post_responses--a603bf05142c----0-----------------------------------)

[Sophia Chen, PhD](/@sophiachen2012?source=post_page---post_responses--a603bf05142c----0-----------------------------------)

[Mar 30, 2025](/@sophiachen2012/thanks-for-sharing-a9cd150656dd?source=post_page---post_responses--a603bf05142c----0-----------------------------------)
    
    
    Thanks for sharing. I'm curious except for occupancy rate and price per night, any customer experience metrics like support tickets / customer feedback are important / incorporated in the model?

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2Fa9cd150656dd&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40sophiachen2012%2Fthanks-for-sharing-a9cd150656dd&user=Sophia+Chen%2C+PhD&userId=528c293fade2&source=---post_responses--a9cd150656dd----0-----------------respond_sidebar------------------)

2

Reply

[![VS](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)](/@valeria.stourm?source=post_page---post_responses--a603bf05142c----1-----------------------------------)

[VS](/@valeria.stourm?source=post_page---post_responses--a603bf05142c----1-----------------------------------)

[Oct 17, 2025](/@valeria.stourm/interesting-to-read-your-approach-in-industry-dac1b16a7352?source=post_page---post_responses--a603bf05142c----1-----------------------------------)
    
    
    Interesting to read your approach in industry. From an academic perspective, this is exactly what we do in our recent research paper: measure the incremental value of a provider to a sharing economy platform, taking into account not only the…more

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2Fdac1b16a7352&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40valeria.stourm%2Finteresting-to-read-your-approach-in-industry-dac1b16a7352&user=VS&userId=cb8a5df25dca&source=---post_responses--dac1b16a7352----1-----------------respond_sidebar------------------)

1

Reply

[![Purvesh Patil](https://miro.medium.com/v2/resize:fill:32:32/0*sUI_UNbhjuZWVjxM)](/@purveshpatil660?source=post_page---post_responses--a603bf05142c----2-----------------------------------)

[Purvesh Patil](/@purveshpatil660?source=post_page---post_responses--a603bf05142c----2-----------------------------------)

[Apr 18, 2025](/@purveshpatil660/great-article-and-thanks-for-sharing-0bde431e148c?source=post_page---post_responses--a603bf05142c----2-----------------------------------)
    
    
    Great article, and thanks for sharing. Do you also measure bookings that are cannibalized from your competitors? If yes, how do you track their data?

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F0bde431e148c&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40purveshpatil660%2Fgreat-article-and-thanks-for-sharing-0bde431e148c&user=Purvesh+Patil&userId=70a7221d4479&source=---post_responses--0bde431e148c----2-----------------respond_sidebar------------------)

Reply

## More from Carlos Sanchez Martinez and The Airbnb Tech Blog

![A Deep Dive into Airbnb’s Server-Driven UI System](https://miro.medium.com/v2/resize:fit:679/format:webp/0*CedYKpSYMIGEiX7m)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----0---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----0---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

by

[Ryan Brooks](/@rbro112?source=post_page---author_recirc--a603bf05142c----0---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

## [A Deep Dive into Airbnb’s Server-Driven UI SystemHow Airbnb ships features faster across web, iOS, and Android using a server-driven UI system named Ghost Platform 👻.](/airbnb-engineering/a-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5?source=post_page---author_recirc--a603bf05142c----0---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

Jun 29, 2021

[A clap icon4.3KA response icon40](/airbnb-engineering/a-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5?source=post_page---author_recirc--a603bf05142c----0---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F842244c5f5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fa-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5&source=---author_recirc--a603bf05142c----0-----------------bookmark_preview----c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

![Pay As a Local](https://miro.medium.com/v2/resize:fit:679/format:webp/1*6K6D4WxFwqlwdtBc6uzczw.jpeg)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----1---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----1---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

by

[Gerum Haile](/@gerum.haile?source=post_page---author_recirc--a603bf05142c----1---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

## [Pay As a LocalHow Airbnb rolled out 20+ locally relevant payment methods worldwide in just 14 months](/airbnb-engineering/pay-as-a-local-bef469b72f32?source=post_page---author_recirc--a603bf05142c----1---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

Jan 12

[A clap icon82A response icon1](/airbnb-engineering/pay-as-a-local-bef469b72f32?source=post_page---author_recirc--a603bf05142c----1---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fbef469b72f32&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fpay-as-a-local-bef469b72f32&source=---author_recirc--a603bf05142c----1-----------------bookmark_preview----c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

![How Airbnb Achieved Metric Consistency at Scale](https://miro.medium.com/v2/resize:fit:679/format:webp/1*rB53PQsJi73IeA-eIeucIg.png)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----2---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----2---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

by

[Robert Chang](/@rchang?source=post_page---author_recirc--a603bf05142c----2---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

## [How Airbnb Achieved Metric Consistency at ScalePart-I: Introducing Minerva — Airbnb’s Metric Platform](/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70?source=post_page---author_recirc--a603bf05142c----2---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

Apr 30, 2021

[A clap icon2.2KA response icon10](/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70?source=post_page---author_recirc--a603bf05142c----2---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff23cc53dea70&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70&source=---author_recirc--a603bf05142c----2-----------------bookmark_preview----c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

![Dynamic Kubernetes Cluster Scaling at Airbnb](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Elojmgc7Y06tItOaLdB0Cw.jpeg)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----3---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c----3---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

by

[David Morrison](/@drmorr-airbnb?source=post_page---author_recirc--a603bf05142c----3---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

## [Dynamic Kubernetes Cluster Scaling at AirbnbAuthors: Evan Sheng, David Morrison](/airbnb-engineering/dynamic-kubernetes-cluster-scaling-at-airbnb-d79ae3afa132?source=post_page---author_recirc--a603bf05142c----3---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

May 23, 2022

[A clap icon550A response icon1](/airbnb-engineering/dynamic-kubernetes-cluster-scaling-at-airbnb-d79ae3afa132?source=post_page---author_recirc--a603bf05142c----3---------------------c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fd79ae3afa132&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdynamic-kubernetes-cluster-scaling-at-airbnb-d79ae3afa132&source=---author_recirc--a603bf05142c----3-----------------bookmark_preview----c76ff0b2_e1c7_43d1_a014_e0ca44dae3c1--------------)

[See all from Carlos Sanchez Martinez](/@carlos.sanchezmartinez?source=post_page---author_recirc--a603bf05142c---------------------------------------)

[See all from The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--a603bf05142c---------------------------------------)

## Recommended from Medium

![Data Engineering Design Patterns You Must Learn in 2026](https://miro.medium.com/v2/resize:fit:679/format:webp/1*0cuVBpD9ZUDcnV3U1mV8cg.png)

[![AWS in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*6EeD87OMwKk-u3ncwAOhog.png)](https://medium.com/aws-in-plain-english?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

In

[AWS in Plain English](https://medium.com/aws-in-plain-english?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

by

[Khushbu Shah](/@khushbu.shah_661?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

## [Data Engineering Design Patterns You Must Learn in 2026These are the 8 data engineering design patterns every modern data stack is built on. Learn them once, and every data engineering tool…](/aws-in-plain-english/data-engineering-design-patterns-you-must-learn-in-2026-c25b7bd0b9a7?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

Jan 5

[A clap icon907A response icon19](/aws-in-plain-english/data-engineering-design-patterns-you-must-learn-in-2026-c25b7bd0b9a7?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fc25b7bd0b9a7&operation=register&redirect=https%3A%2F%2Faws.plainenglish.io%2Fdata-engineering-design-patterns-you-must-learn-in-2026-c25b7bd0b9a7&source=---read_next_recirc--a603bf05142c----0-----------------bookmark_preview----6e985ac7_79de_435f_9172_1e88797663b7--------------)

![Building AI Agents in 2026: Chatbots to Agentic Architectures](https://miro.medium.com/v2/resize:fit:679/format:webp/1*QOF4rZaV-KHzmvnBFsiOPQ.png)

[![Level Up Coding](https://miro.medium.com/v2/resize:fill:20:20/1*5D9oYBd58pyjMkV_5-zXXQ.jpeg)](https://medium.com/gitconnected?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

In

[Level Up Coding](https://medium.com/gitconnected?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

by

[Gaurav Shrivastav](/@gaurav21s?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

## [Building AI Agents in 2026: Chatbots to Agentic ArchitecturesThis is the engineering blueprint for building production-ready agentic systems that actually work.](/gitconnected/the-2026-roadmap-to-ai-agent-mastery-5e43756c0f26?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

Jan 22

[A clap icon507A response icon7](/gitconnected/the-2026-roadmap-to-ai-agent-mastery-5e43756c0f26?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F5e43756c0f26&operation=register&redirect=https%3A%2F%2Flevelup.gitconnected.com%2Fthe-2026-roadmap-to-ai-agent-mastery-5e43756c0f26&source=---read_next_recirc--a603bf05142c----1-----------------bookmark_preview----6e985ac7_79de_435f_9172_1e88797663b7--------------)

![Screenshot of a desktop with the Cursor application open](https://miro.medium.com/v2/resize:fit:679/format:webp/0*7x-LQAg1xBmi-L1p)

[![Jacob Bennett](https://miro.medium.com/v2/resize:fill:20:20/1*abnkL8PKTea5iO2Cm5H-Zg.png)](/@jacobistyping?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[Jacob Bennett](/@jacobistyping?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

## [The 5 paid subscriptions I actually use in 2026 as a Staff Software EngineerTools I use that are (usually) cheaper than Netflix](/@jacobistyping/the-5-paid-subscriptions-i-actually-use-in-2026-as-a-staff-software-engineer-b4261c2e1012?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

Jan 18

[A clap icon2.7KA response icon68](/@jacobistyping/the-5-paid-subscriptions-i-actually-use-in-2026-as-a-staff-software-engineer-b4261c2e1012?source=post_page---read_next_recirc--a603bf05142c----0---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fb4261c2e1012&operation=register&redirect=https%3A%2F%2Fjacob.blog%2Fthe-5-paid-subscriptions-i-actually-use-in-2026-as-a-staff-software-engineer-b4261c2e1012&source=---read_next_recirc--a603bf05142c----0-----------------bookmark_preview----6e985ac7_79de_435f_9172_1e88797663b7--------------)

![Apple Liquid Glass after 4 months](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Iu0QDrOp4TOydC0aEkV-2Q.png)

[![Michal Malewicz](https://miro.medium.com/v2/resize:fill:20:20/1*149zXrb2FXvS_mctL4NKSg.png)](/@michalmalewicz?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[Michal Malewicz](/@michalmalewicz?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

## [I was wrong about Liquid Glass.It’s actually amazing — here’s why.](/@michalmalewicz/i-was-wrong-about-liquid-glass-751ce510f5ec?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

Oct 19, 2025

[A clap icon1.5KA response icon43](/@michalmalewicz/i-was-wrong-about-liquid-glass-751ce510f5ec?source=post_page---read_next_recirc--a603bf05142c----1---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F751ce510f5ec&operation=register&redirect=https%3A%2F%2Fmichalmalewicz.medium.com%2Fi-was-wrong-about-liquid-glass-751ce510f5ec&source=---read_next_recirc--a603bf05142c----1-----------------bookmark_preview----6e985ac7_79de_435f_9172_1e88797663b7--------------)

![Stanford Just Killed Prompt Engineering With 8 Words \(And I Can’t Believe It Worked\)](https://miro.medium.com/v2/resize:fit:679/format:webp/1*va3sFwIm26snbj5ly9ZsgA.jpeg)

[![Generative AI](https://miro.medium.com/v2/resize:fill:20:20/1*M4RBhIRaSSZB7lXfrGlatA.png)](https://medium.com/generative-ai?source=post_page---read_next_recirc--a603bf05142c----2---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

In

[Generative AI](https://medium.com/generative-ai?source=post_page---read_next_recirc--a603bf05142c----2---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

by

[Adham Khaled](/@adham__khaled__?source=post_page---read_next_recirc--a603bf05142c----2---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

## [Stanford Just Killed Prompt Engineering With 8 Words (And I Can’t Believe It Worked)ChatGPT keeps giving you the same boring response? This new technique unlocks 2× more creativity from ANY AI model — no training required…](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--a603bf05142c----2---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

Oct 19, 2025

[A clap icon23KA response icon618](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--a603bf05142c----2---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F8349d6524d2b&operation=register&redirect=https%3A%2F%2Fgenerativeai.pub%2Fstanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b&source=---read_next_recirc--a603bf05142c----2-----------------bookmark_preview----6e985ac7_79de_435f_9172_1e88797663b7--------------)

![6 brain images](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Q-mzQNzJSVYkVGgsmHVjfw.png)

[![Write A Catalyst](https://miro.medium.com/v2/resize:fill:20:20/1*KCHN5TM3Ga2PqZHA4hNbaw.png)](https://medium.com/write-a-catalyst?source=post_page---read_next_recirc--a603bf05142c----3---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

In

[Write A Catalyst](https://medium.com/write-a-catalyst?source=post_page---read_next_recirc--a603bf05142c----3---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

by

[Dr. Patricia Schmidt](/@creatorschmidt?source=post_page---read_next_recirc--a603bf05142c----3---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

## [As a Neuroscientist, I Quit These 5 Morning Habits That Destroy Your BrainMost people do #1 within 10 minutes of waking (and it sabotages your entire day)](/write-a-catalyst/as-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226?source=post_page---read_next_recirc--a603bf05142c----3---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

Jan 14

[A clap icon29KA response icon500](/write-a-catalyst/as-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226?source=post_page---read_next_recirc--a603bf05142c----3---------------------6e985ac7_79de_435f_9172_1e88797663b7--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F3efe1f410226&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fwrite-a-catalyst%2Fas-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226&source=---read_next_recirc--a603bf05142c----3-----------------bookmark_preview----6e985ac7_79de_435f_9172_1e88797663b7--------------)

[See more recommendations](/?source=post_page---read_next_recirc--a603bf05142c---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----a603bf05142c---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----a603bf05142c---------------------------------------)

[About](/about?autoplay=1&source=post_page-----a603bf05142c---------------------------------------)

[Careers](/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----a603bf05142c---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----a603bf05142c---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----a603bf05142c---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----a603bf05142c---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----a603bf05142c---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----a603bf05142c---------------------------------------)