# ProfAI
Github repository for the Hack-Nation AI Hackathon 2025

Project Report: 
Our team chose to implement challenge 8 and we delivered an MVP of ProfAI, an AI instructor that begins 
each unit with a brief, structured lesson (ex: five bullets and a small example) and then transitions into an 
interactive Q&A, where learners ask clarifying questions via chat. To support real users, we added a 
login/sign-up flow backed by MongoDB with bcrypt for secure credential storage and basic engagement 
tracking. We then implemented the teaching logic behind a lightweight Flask API and wired the web client 
to it. Finally, we resolved CORS and port configuration issues to ensure reliable browser-to-API 
communication. 

Frontend: HTML/CSS/JavaScript served with a simple local server.  
Backend: Flask for the chatbot API and Node/Express for auth. Data: MongoDB (local or Docker) with 
bcrypt for passwords. Model: Google’s Gemini (1.5 Flash) for lessons and Q&A. 

Using small, clear endpoints made testing and changes quite simple, which let us iterate quickly. Gemini 
produced short, clear lessons with minimal prompt tuning, and with a tiny formatter the content is now 
displayed as clean, scannable bullets. For the authentication and data components, MongoDB with a 
simple user model and bcrypt for secure password hashing was straightforward and dependable, so we 
didn’t get bogged down there. Moreover, because the UI stayed minimal and all the configurations lived in 
a single .env, the setup was quick and there was less to break. Overall, a fast model and a lightweight 
stack kept our feedback loop tight. 

Early on, CORS preflight errors and port conflicts blocked our requests, so nothing reached the API. On 
top of that, the setup di erence between Mac and Windows slowed testing and made instructions drift. 
We also had to line up routes and environment variables across the frontend, Flask, and Node to keep 
calls consistent end-to-end. Overall, all of this had to happen without changing the existing UI, so we 
debugged under tighter constraints. 

Before coding, we split responsibilities between frontend and backend and agreed on must-haves vs. 
nice-to-haves to establish what's necessary for the MVP. With the scope clear, we built the login and 
signup flows, then wired the chatbot and prompts for our two teaching units. Most of our time went into 
untangling CORS, port, and API key issues and verifying everything on both Mac and Windows. To make 
hando s easier, we documented platform-specific setup steps and environment configuration, enabling 
any of our team members to run the app on their machine for debugging and development purposes. 
