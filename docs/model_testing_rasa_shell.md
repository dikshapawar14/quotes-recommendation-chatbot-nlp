# Story: Model Testing Using Rasa Shell

The chatbot model is tested using the Rasa shell, which provides a command-line interface to interact with the chatbot.

## Starting the Rasa Shell

The following command is used to start the shell:

rasa shell

This command loads the trained chatbot model and allows developers to interact with it by typing user messages.

## Testing Process

During testing, different types of user inputs are provided such as:

- Motivational quote requests
- Inspirational quotes
- Humorous quotes
- Love quotes
- Success quotes
- Greetings and farewell messages

Example interaction:

User: Give me a motivational quote  
Bot: Believe you can and you are halfway there.

User: Bye  
Bot: Goodbye! Have a great day.

## Purpose of Testing

The testing process helps ensure that:

- The correct intent is detected
- The correct quote category is returned
- The conversation flow works properly

It also helps identify errors such as misclassification or missing training data.