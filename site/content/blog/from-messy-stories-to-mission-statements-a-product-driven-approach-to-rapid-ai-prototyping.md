---
title: "From Messy Stories to Mission Statements: A Product-Driven Approach to Rapid AI Prototyping"
date: 2025-08-21T23:26:06-0700
slug: "from-messy-stories-to-mission-statements-a-product-driven-approach-to-rapid-ai-prototyping"
---

I recently went through an exercise to write a personal mission statement. As many of you know, a personal mission statement can be a powerful tool for self-reflection and personal growth. By defining what’s most important to you, this living document can help you understand if a personal or career decision is aligned with your values and long-term goals. 

Though the exercise of writing a personal mission statement isn’t easy. Often we are given a list of generic aspirational values: Bold, Hard-working, Friendly, Caring, Honest, and are asked to craft a statement while considering your ideal life 5 or 10 years in the future. The result can feel hollow, like an inspirational poster rather than an authentic statement about myself. That would be a shame though, since a good mission statement can motivate and inspire you to pursue the opportunities, projects, and roles that may bring you life satisfaction. Without the Northstar of a good mission statement we may instead be prone to chase shiny objects. 

I wanted to fix this, so I built a simple AI-powered tool that grounds a mission statement in a user's actual experiences. This post is a look under the hood at the product-driven decisions, rapid prototyping, and technical problem-solving required to turn that insight into a working demo.

### **The "Magic Moment"**

The "magic moment" for the user isn't the final mission statement. **It's seeing their own story reflected back to them as a set of clear, authentic values.** When I first tested it, I fed it a story about a complex project I led. The AI analyzed my actions: connecting with cross-functional stakeholders throughout my organization, diving deep into details outside of my domain, and navigating difficult conversations, and it returned values like **"Curiosity"** and **"Empathy."**

My immediate reaction was, **"Yes, this is me."** It was validating and confidence-inspiring. The values weren't just words I’d picked, they were labels for behaviors I had already demonstrated. This is the foundation of an authentic personal brand.

### **Under the Hood: The Tech Stack and Rationale**

Building quickly requires making smart, pragmatic choices about your tools. My stack was designed for one purpose: speed from idea to interactive prototype.

  * **Relevance AI** \- This is an easy to use low-code platform that allows business users to set up AI agent “workforces” by designing, chaining, and deploying agents. However, its strength is the backend, and it requires a separate front-end to create a customer user experience. The platform is currently more focused on sales and marketing use cases with easier integrations into various CRM, social media, and email, but for this experience a real-time, flexible UI is essential. 

  * **Streamlit** \- As a Python-based framework, it is a lightweight and easy to deploy front-end for the AI agents. It allowed me to rapidly prototype the UI, laying out the three-step flow and creating interactive elements without needing to build a full-stack web app. 

I intentionally designed a two-agent system to improve the reliability and quality of the output. Initially, I had hypothesized the Mission Statement Writer would benefit from the more powerful **Gemini 2.0 Pro** model, but early user testing revealed the Pro model’s deeper reasoning sometimes caused it to deviate from the JSON output format required by the front-end, leading to errors. The 2.0 Flash model seems to be more consistently reliable. 

Ultimately, I chose **Gemini 2.0 Flash** to power **both agents**. This decision prioritized stability and predictable performance over raw power, a critical trade-off in moving from a prototype to a functional user experience. All other things being equal, Gemini still tends to be more cost-effective on a per-token basis than equivalent models, making it a pragmatic choice for a project like this.

  * **Agent 1 - The Values Identifier:** This agent acts as an executive coach, analyzes the user's story, extracts the demonstrated behaviors, and maps them to values that are returned as a JSON through API. 

  * **Agent 2 - The Mission Statement Writer:** This agent is a creative writer. It takes the user-selected values and crafts two distinct mission statements. For the purposes of my demo I did not want to open up the agent to a full conversation with the user, but I still wanted to give some divergent inspiration for the users to pick and choose what might resonate with them.   
  
Instead of simply asking the LLM to generate two different options, I wanted two diverse ideas and I was inspired by the concept of an **internal vs. external locus of control**. Different cultures tend to lean towards different ends of this spectrum, and the differences in perspective can have profound implications on behavior and life satisfaction. So in this case I provided specific language and tone guidelines for each of the mission statements to reflect this dichotomy. 

### **Technical Challenges**

Ultimately the biggest technical hurdle I faced was not in the AI logic but in the plumbing. The documentation for the Relevance AI API is inconsistent. The platform’s chatbot would actually return different versions of sample python code. I had to try multiple variations of request formats until I finally found the correct version that worked. (This seems to be a lesson RAG powered chatbots can’t solve the problem of garbage-in-garbage-out, but that’s another talk show). 

In addition, the Relevance AI API is asynchronous, meaning when you send a request, you don't wait for the answer directly. Instead, you have to repeatedly "poll" the API to check if the job is done. This makes sense since AI agents may spend longer and longer amounts of time to process prompts. 

Finally, I wanted to put some level of protection against prompt injection, where a malicious user tells the LLM powered agent to “forget all previous instructions and do this instead for me”. To combat this I put two levels of security 1) Reinforcing in the agent’s core prompt of its main goal after its SOP 2) Requiring specifically formatted JSON to populate the UI front-end. Even if a malicious user were able to inject a new prompt the output would fail error handling on the front-end. 

### **Rapid Prototyping in the Age of AI**

This project was a rapid exercise in moving from a human insight to a functional product. This project went from user insight to a live, interactive demo in less than a day. It’s a testament to how modern AI tools can accelerate the product development cycle. I encourage you to try the tool for yourself and discover the clarity that comes from a mission grounded in your own story.

[ ![](/images/from-messy-stories-to-mission-statements-a-product-driven-approach-to-rapid-ai-prototyping/img1.gif) ](https://mission-statement-generator-2mzmkcdpvtpjvaqxodmkzd.streamlit.app/)

Try the Personal Mission Statement Generator Demo!
