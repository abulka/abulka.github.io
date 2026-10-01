---
title: "Conversation Starter"
date: 2026-10-01
type: docs
draft: false
tags: ["React Native", "Expo", "Mobile", "Android", "Software Product"]
---

## Conversation Starter

An app that helps you start conversations. Stuck for something to say? Press a button and it pulls up a random joke to break the ice, a piece of stoicism to discuss, or an optimistic or poetic saying to lift the mood. Copy any of them to share.

![Conversation Starter](/projects/mobile-apps/images/conversation-starter-promo.png)

- Download for Android on [Google Play](https://play.google.com/store/apps/details?id=com.wware.conversationstarter)
- Use it in your browser as a [mobile web app](https://convstart-4774e.web.app/) (installable as a PWA)
- Code: [github.com/abulka/conversation-starter](https://github.com/abulka/conversation-starter)

## What it does

Four buttons, one purpose: give you something interesting to say.

- **Tell me a joke** – a random joke to break the ice.
- **Give me Stoicism** – a stoic saying from Marcus Aurelius, Seneca and Epictetus to spark a deeper conversation.
- **Optimistic Saying** – a short upbeat line to lift the mood.
- **Poetic Saying** – a memorable line from poets and writers such as Tennyson, Dickinson and Mary Oliver.

Each press picks a new item and avoids repeating the one you just saw, and a Copy button puts the current saying on your clipboard so you can share it.

![Conversation Starter joke screen](/projects/mobile-apps/images/conversation-starter-1.png)
![Conversation Starter anti-gravity joke screen](/projects/mobile-apps/images/conversation-starter-2.png)

## One app, three homes

Conversation Starter is built once with Expo and React Native and shipped three ways from the same codebase:

- an **Android app** on the Google Play Store, built and submitted with EAS
- an installable **mobile web app** (PWA) hosted on Firebase Hosting, so you can add it to your phone's home screen from the browser
- a simple **landing page** at [abulka.github.io/conversation-starter-website](https://abulka.github.io/conversation-starter-website/)

## Under the hood

The app is deliberately small: a single screen holding the sayings and a few buttons. It is a React functional component using `useState` hooks to remember the current text and the last item shown, so the random picker never repeats itself.

Here is the main flow in [Plain Text Diagram](/blog/plain-text-diagrams) notation:

```plaintext
Use Cases:
  Sequence: Display a random joke
    selectRandomItem(jokes, lastJokeNumber, setLastJokeNumber, 'joke') [App.js]
      [do while (number === lastBlahNumber)]
      -> Math.random()
          generates a random number
          < number
      -> setLastJokeNumber(number: number) [App.js]
          updates the last number used
      -> setTextOut(item: string) [App.js]
          updates the displayed text output

  Sequence: Render the application UI
    render() [App.js]
      -> Button() [App.js]
          [onPress: selectRandomItem(jokes, ...)]
          displays the "Tell me a joke" button
      -> Button() [App.js]
          displays the "Give me Stoicism" button
      -> Button() [App.js]
          displays the "Optimistic Saying" button
      -> Button() [App.js]
          displays the "Poetic Saying" button
```

## Technologies

| Description | Technology |
| --- | --- |
| Framework | [Expo](https://expo.dev/) / [React Native](https://reactnative.dev/) |
| UI components | [React Native Paper](https://callstack.github.io/react-native-paper/) |
| Icons | [Material Community Icons](https://github.com/oblador/react-native-vector-icons) |
| Clipboard | [expo-clipboard](https://docs.expo.dev/versions/latest/sdk/clipboard/) |
| Android build | [EAS Build](https://docs.expo.dev/build/introduction/) |
| Web hosting | [Firebase Hosting](https://firebase.google.com/docs/hosting) |
