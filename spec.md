# **Intelligent Standup Bot Exercise Requirements**

## **Overview**

Create an intelligent assistant that helps collect daily standup updates through Slack. The system should focus on natural conversations and reducing user workload through automated drafting.

Start with baseline requirements and then work on escalating additional requirements. If you have additional ideas for the standup bot you can go ahead and implement it. 

## **Update Structure**

The standup updates should cover: accomplishments since last standup, plans for today, and any blockers or challenges currently faced.

## **Feature Requirements**

### **1\. Intelligent Conversation with Memory**

**Base Requirements**

* Natural language collection of updates  
* Parse accomplishments, plans, and blockers from free-form text, even when combined (e.g., User: "Fixed the auth bug from yesterday and started on the API tests. Still waiting on DB access but will continue with mock data for now")  
* Smart follow-up questions when responses are vague or unclear  
* Proactively identify potential blockers from responses (e.g., If user mentions "waiting for review" or "need input from team")  
* Remember user's preferred writing style (bullet points vs. paragraphs) for the update

**Escalating requirements for additional challenges**

1. Memory Across Sessions  
   * Remember and follow up on previous day's updates (e.g., "Yesterday you planned to finish validation. Did you complete that?")  
   * Check on previously reported blockers (e.g., "Is the DB schema issue from yesterday resolved?")  
2. Pattern Recognition  
   * Identify recurring blockers across multiple updates for potential escalation (e.g., "I notice this DB schema issue has been blocking you for 3 days now. Should this be escalated?")  
   * Help surface systemic issues that need manager attention (e.g., "Infrastructure access has been mentioned as a blocker in most of your updates this week")  
3. Flow Memory  
   * Learn how users prefer to give their updates (e.g., Some prefer to list all items at once, others prefer a dialogue)  
   * Adapt question order based on user's natural flow  
   * Remember if user prefers to start with GitHub drafts or free-form updates

### **2\. Drafting & Integration**

The system should help reduce user workload by automatically drafting updates based on their work activity.

**Base Requirements**

* GitHub integration using the actual GitHub API (no mocked data). Use the Github project you are using to build the solution to test and demonstrate the solution.  
* Draft updates using GitHub activity from the last 24 hours  
  * Can include any relevant activity: commits, PRs, reviews, comments, etc.  
* Allow user to edit/modify drafted content

**Escalating requirement for additional challenge**

* Linear integration for task tracking (use the linear project you are using to breakdown this project into tasks and sub-tasks for this purpose)  
* Combine GitHub and Linear data for comprehensive drafts

### **3\. User Experience**

**Base Requirements**

* Build using either Slack or Web chat interface  
* Daily notification to trigger standup updates  
* Ability to collect updates for a specific date

**If Time Permits**

* Build additional interface (Slack or Web chat, whichever wasn't chosen for base)  
* Organize daily updates in threads/conversations

## **Demo Instructions**

The demo should demonstrate building of features through two update collections:

1. First Update Notification & Collection This demonstrates basic functionality:  
   * GitHub integration setup and data fetching (include linear based on your progress)  
   * Natural language update collection  
   * Draft generation from GitHub activity  
   * Base conversation intelligence (follow-ups, blocker identification)  
   * Format preferences (bullets vs paragraphs)  
2. Next Day's Update Notification & Collection  
   * Using established GitHub integration  
   * Any implemented memory features:  
     * Referring to previous day's plans  
     * Following up on mentioned blockers  
     * Using learned format preferences  
     * Pattern recognition if implemented

Each step should show the natural conversation flow and core features, with any additional implemented capabilities demonstrated in context rather than as separate features.

## **Suggested Agent Frameworks**

**1\. CrewAI**

* Orchestrating collaboration among AI agents  
* Excellent for complex multi-agent workflows

**2\. Langchain**

* Streamlined development for LLM-powered applications  
* Strong memory and prompt management

**3\. Microsoft AutoGen**

* Building advanced AI agents  
* Sophisticated agent-to-agent communication

**4\. OpenAI Swarm**

* Lightweight multi-agent orchestration  
* Efficient task distribution and coordination

Additional Stack: FastAPI, PostgreSQL, Slack Bolt SDK

 **Appendix: Project Setup**

Project Tracking \- We will use Linear to break down and track your assignment progress. Please create a project in linear.app so you can track the work items there and also use it as integration for the bot.

Source Control \- Create a GitHub repository to develop and share your progress on this assignment. You will use the same repository and Linear project when building the GitHub/Linear integrations required in the exercise.

