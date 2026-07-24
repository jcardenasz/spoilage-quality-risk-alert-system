# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Proof of Concept (POC) for a Raw Material Quality & Spoilage Risk Alert System.
The system uses n8n for workflow orchestration, an AI agent (Google Gemini or Groq) for risk evaluation,
and simulated data to demonstrate the concept.

## Architecture

As outlined in PRD_Spoilage_Risk_Alert_POC.md, the system consists of:

1. Simulated batch data source (mock dataset)
2. n8n workflow for:
   - Ingestion (scheduled or manual trigger)
   - Preprocessing (compute deviations from ideal storage ranges)
   - AI risk agent (LLM-based evaluation)
   - Risk-based routing (alert for high risk, log for all)
3. Alerting (Slack or email) for high-risk batches
4. Risk log/dashboard (Google Sheets or Airtable) for history

## Development Setup

Since this is a POC and the implementation is primarily in n8n (a low-code/no-code platform),
the development involves:

- Setting up n8n (via [n8n.io](https://n8n.io/)) using docker:
  * Docker: `docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n`
- Creating an n8n workflow that follows the steps in the PRD.
- Setting up API keys for Google Gemini (or Groq) and storing them as n8n environment variables.
- Configuring nodes for data storage (Airtable) and alerting (email).

## Common Tasks

Once the n8n workflow is set up:

- **Generating mock data**: The PRD describes a mock dataset. You may create a script (e.g., in Python or JavaScript)
  to generate sample batch records and insert them into the data source (Google Sheets/Airtable) or use n8n's built-in
  capabilities to generate mock data via a Function or HTTP Request node.

- **Running the workflow**: 
  * In n8n, you can trigger the workflow manually or set up a cron trigger for scheduled runs.
  * To test, you can execute the workflow from the n8n editor.

- **Viewing logs**: Check the connected Google Sheet or Airtable base for the risk log.

- **Testing the AI agent**: You can test the AI agent node in isolation by providing sample input data
  and checking the output for risk percentage, level, factors, and recommended action.

## Future Implementation Notes

As the project evolves beyond the POC, we may introduce:

- Custom code nodes in n8n for preprocessing or other logic.
- A separate service for the AI agent if we move beyond the free tier limits.
- A frontend dashboard (as mentioned in the PRD) using Vercel for deployment.
- (Phase 2) A conversational Q&A agent using n8n AI Agent with read access to the risk log.

## Important Files

- `PRD_Spoilage_Risk_Alert_POC.md`: The main product requirements document.
- `.gitignore`: Standard ignore file for Node.js projects (to be expanded as we add code).

## Next Steps

1. Set up n8n and create the workflow as per the PRD.
2. Generate or acquire simulated batch data.
3. Configure the AI agent node with the Google Gemini or Groq API.
4. Set up the data storage and alerting nodes.
5. Test the end-to-end workflow with sample data.
6. Implement the conversational Q&A agent (Phase 2).

## Always

Write spec.md and other files so the user has information about the process and where he can see decisions, tasks made, prompts and all relevant information for a SDD project.