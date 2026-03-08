# Story 2: Setting Up the Rasa Project

The Quotes Recommendation Chatbot is built using the Rasa framework for natural language understanding and dialogue management.

## Project Initialization

The project is initialized using the following command:

rasa init

This command automatically generates a structured chatbot project with predefined directories and configuration files.

## Project Structure

data/
Contains training datasets such as intents, stories, and rules.

actions/
Stores custom Python actions used to extend chatbot functionality.

models/
Stores trained chatbot models generated during training.

tests/
Contains test stories used for validating chatbot behavior.

config.yml
Defines the NLP pipeline and dialogue management policies.

domain.yml
Defines intents, responses, entities, and actions used by the chatbot.

credentials.yml
Configures communication channels such as REST API.

endpoints.yml
Defines service endpoints for external integrations.

## Purpose

This structure provides a standardized framework for building, training, and deploying the chatbot efficiently.