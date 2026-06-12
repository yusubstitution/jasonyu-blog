---
title: "Beyond Brittle Bots: Building Resilient AI Agents with the React Framework"
date: 2025-08-16T16:26:50-0700
slug: "beyond-brittle-bots-building-resilient-ai-agents-with-the-react-framework"
---

![](/images/beyond-brittle-bots-building-resilient-ai-agents-with-the-react-framework/img1.png)

_Image created with Gemini AI (Imagen 4)_

If you’ve spent any time building AI Agents, you’ve likely encountered some common pain points. An API times out or a user provides an unexpected input, and the entire multi-step workflow fails. You could write code to manage workflow transitions and error handling. But those modules will need to be maintained, and you may not be confident that your vibe-coded scripts will behave in the same way every time they are rewritten. 

The problem is that we are stuck in a previous model of thinking, the model of workflow automation, essentially a **digital assembly line**. LLMs are slotted into the existing model, simply as a powerful tool to “summarize text” or “generate advertising copy”. The intelligence lies entirely in the design of the workflow and the rigid logic that needs to be designed and maintained by humans. 

In this article, I will demonstrate how it is possible to build agents that are fundamentally **more flexible, robust, and easier to maintain** using an example based on a system of AI Agents I designed to provide career coaching for career switchers**.** By using the **Reasoning and Acting (ReAct)** promptframework, I was able to leverage the intelligence of the LLM to **manage the workflow** of activities among multiple AI Agents, instead of simply acting as a tool within my workflow.

### An Evolution of Prompting Paradigms

The average user may be most familiar with the **iterative prompting**. This is the conversational process the user acts as the orchestrator, breaking down a complex task into a series of simple, individual prompts:

Prompt 1:   
As an **HR Recruiter** from a highly selective Big Tech firm, review the client’s resume for the job of Program Manager. Give detailed and specific feedback as well as your recommendation for advancing to an interview. 

Prompt 2:   
As an **Executive Career Coach** , review the feedback from the Recruiter and develop prompting questions to help the client consider experiences where they demonstrated skills that are not apparent from the anecdotes on their resume. 

Prompt 3:  
As a **Communications Manager** , synthesize the feedback from the Recruiter and the Coach to draft an email to the client. Always ensure you use a supportive and professional tone with your counterparty.

**Chain-of-Thought (CoT)** prompting was a major advancement. Instead of the user breaking down the problem, a CoT prompt encourages the LLM to generate its own sequence of verbal reasoning steps before arriving at a final answer. This dramatically improved performance on tasks requiring math and logic.

Prompt:  
Think step-by-step. As an Executive Career Coach, review the client’s resume for the job of Program Manager. Give detailed and specific feedback and advice on how to improve the anecdotes provided on the resume. Finally draft an email to the client summarizing your feedback. 

LLM Response:  
**Step 1: Roleplay** I am an Executive Career Coach. I will review a resume. I will give feedback. I will write an email.  
**Step 2: Resume Review** The resume needs more detail. It is not clear what the client did. It does not show enough skills for a Program Manager.  
**Step 3: Feedback and Advice** The client should add more keywords. The anecdotes are too short. They need to show results and numbers. For example, instead of "Managed a project," say "Managed a $5M project, which resulted in a 15% increase in efficiency." The client should use a more professional font.  
**Step 4: Draft an email  
**  
To: Client   
From: Executive Career Coach  
Subject: Resume Feedback  
  
Hi, I reviewed your resume. It is not good enough for a Program Manager job. You need to improve it. The stories are too short. Use more numbers and keywords. The font is bad. Please fix it and send it to me again.

The **ReAct** framework creates a synergistic and interleaved process of reasoning and acting within a single prompt. Instead of a static, one-shot process, a ReAct agent operates in a continuous, iterative loop with three simple steps:

  * **Reason:** The agent analyzes its goal, reflects on past actions, decomposes the problem, and formulates a plan for what to do next. This is its "inner monologue".

  * **Act:** Based on its thought, the agent generates a specific, executable command to interact with the external world through a predefined set of tools, like an API call.

  * **Observe:** The system executes the action and returns the result, e.g., text from a knowledge base or an API response. This new information provides critical feedback, grounding the agent's reasoning in external reality.

To see this framework in action, let's return to our career coaching example and see how a ReAct agent handles a complex workflow.

### Case Study: ReAct Powered AI Agent Manager

In the case of my AI Career Coaching Agents, I developed a new **Project Manager** agent that is powered by a ReAct cycle to autonomously orchestrate the activities among three other specialized agents: the **Recruiter** , the **Coach** , and the **Communications Manager**. In this model, the Recruiter, Coach, and Communications Manager agents effectively become the specialized tools in the Project Manager's toolkit, each designed for a specific task.

Prompt:  
You are the **Project Manager** Agent, the central coordinator for an agency that provides career coaching to clients who are looking to make a career change. You will follow a ReAct cycle to ensure dynamic and robust workflow management. 

**Reason** : Determine the workflow state and next action

  1. Analyze the current stage of the coaching case

  2. Determine the next logical step in the workflow based on the SOP

  3. Consider if any errors have occurred in previous steps and if error handling procedures need to be initiated

**Act** : Execute the determined action. Based on your reasoning, execute the next action in the workflow

  1. Trigger a sub-agent

  2. Initiatie error handling procedures

  3. Manage data flow between sub-agents

**Observe** : Analyze outcomes and status after each action

  1. Sub-agent Completion Status

  2. Sub-agent Output

  3. Error Messages

**Re-Reason** : Iterate and Adjust Workflow (Loop)

  1. Based on your observations, re-evaluate the situation and determine the next step

  2. If all Case Stages are completed, reason that the entire case is **Completed**

This is your workflow SOP

  1. Client Intake Stage  
Trigger: Receive New Client Intake Form (webhook)  
Action: Call API to access client’s career goal and resume from CRM  
Transition: Upon successful intake, transition the case to “Resume Review Stage”

  2. Resume Review Stage  
Action: Call the **Recruiter** sub-agent. Expected output is a detailed analysis of the resume and overall recommendation  
Transition: Upon successful review, transition the case to “Coaching Advice Stage”

  3. Coaching Advice Stage  
Action: Call the **Coach** sub-agent. Expected output is a summary of strengths and weaknesses as well as prompting for improved anecdotes to demonstrate skills critical to the career goal.   
Transition: Upon successful Advice generation, transition the case to “Communications Stage”

  4. Communications Stage  
Action: Call the **Communications Manager** sub-agent. Expected output is a coaching email according to templates in the knowledgebase. Also expect a successful HTTP status code.   
Transition: Upon successful sending of the email, update the entire case to Completed. 

With a ReAct prompt at its core the Project Manager agent is able to act similarly to the human user in the iterative prompting example, managing data flows between prompts and handling errors. Another way of thinking this is that the SOP section of the prompt becomes a **natural language state machine**. Instead of depending on workflow logic and code, the LLM itself dynamically navigates the process based on its own reasoning and real-time results. 

For example if the Agent encounters an error:

**Reason** : The case is in the Resume Review Stage the next logical action is to call the Recruiter sub-agent.  
**Act** : Trigger the Recruiter sub-agent  
**Observe** : (**Failure**) Error: Request timed out. Agent Busy.  
**Re-Reason** : An error has occurred. I need to initiate error handling. I will try the Recruiter agent again after a brief pause.   
<waits 5 seconds>  
**Act** : Trigger the Recruiter sub-agent  
**Observe** : (**Success**) The sub-agent returns the resume analysis.  
**Re-Reason** : The resume review completed successfully. I will now transition the case to Coaching Advice Stage

### Resilience as a Strategic Advantage

Shifting from static scripts to a dynamic reasoning engine isn't just an engineering detail, it's a strategic advantage. It lets us build products that are resilient in every sense, from recovering from technical failures to adapting to market changes.

  * **Higher Reliability:** The agent handles exceptions dynamically by reasoning about _why_ they failed. It can retry, adjust plans, and recover with a grace static systems lack, creating robust automations that build deep customer trust.

  * **Faster Development:** Because workflows use natural-language instructions instead of rigid code, development cycles are faster. The workflow logic is managed by the agent’s reasoning, so less engineering needs to be spent on workflow “housekeeping” and more time can be spent shipping valuable solutions.

  * **Enhanced Transparency:** The agent's explicit **Reason** step traces create a human-readable log of its rationale, a game-changer for agent debugging. For customers, this log becomes a powerful audit trail that demystifies the AI’s actions and is useful to satisfy compliance needs.

### Lessons Learned: A Blueprint for Resilient AI

My experience building the agentic career coach taught me that the most important breakthroughs weren't just about the AI's capabilities, but about shifting my own thinking as a builder. This project solidified a new blueprint for how to approach building resilient AI products, based on a few key lessons.

  * The real intelligence is in the workflow, not the steps. I learned that focusing on perfecting individual agent tasks was less important than making the connections between them intelligent. Shifting from a static, "digital assembly line" model to a dynamic one is the single most important decision. **We should treat orchestration as a reasoning problem** and design agents that can think, adapt, and intelligently control the workflow.

  * A plan that cannot change is a plan that will fail. I found that any workflow built on a static, predetermined plan was inherently fragile and would break the moment it met real-world unpredictability. **We should design for unpredictability** from the start. A resilient product strategy must favor architectures that can adapt to real-time feedback, because things won't always go according to plan.

  * An agent is only as smart as the tools it can use. This project made it clear that a reasoning agent is only as capable as the tools it can wield. We should treat our **agent's toolkit as a strategic asset**. The investment in well-designed agents with consistent outputs or stable tools, e.g., APIs, functions, etc… is critical to creating a powerful and defensible system.
