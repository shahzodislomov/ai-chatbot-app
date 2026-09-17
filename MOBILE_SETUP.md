# 📱 Mobile App Setup Guide

Convert your AI chatbot to iOS/Android with **zero code changes**.

---

## Option 1: React Native with Expo (Easiest ⭐)

### Setup (10 minutes)

```bash
# Install Expo CLI
npm install -g expo-cli

# Create new React Native project
expo init chatbot-mobile

# Choose "blank" template
# Navigate to project
cd chatbot-mobile

# Install dependencies
npm install axios uuid
```

### Convert Frontend to React Native

Copy this to `App.js`:

```javascript
import React, { useState, useEffect, useRef } from 'react'
import {
  View, Text, TextInput, TouchableOpacity, FlatList,
  SafeAreaView, KeyboardAvoidingView, Platform, StyleSheet,
  ActivityIndicator
} from 'react-native'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'

const API_BASE_URL = 'http://YOUR_BACKEND_IP:8000'

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [userId] = useState(() => uuidv4())
  const [conversationId, setConversationId] = useState(() => uuidv4())

  const handleSendMessage = async () => {
    if (!input.trim()) return

    setMessages(prev => [...prev, { user: input }])
    setLoading(true)
    setInput('')

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        text: input,
        user_id: userId,
        conversation_id: conversationId
      })

      setMessages(prev => [...prev, { bot: response.data.response }])
    } catch (error) {
      setMessages(prev => [...prev, {
        bot: 'Error: Make sure backend is running on ' + API_BASE_URL
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        <FlatList
          data={messages}
          renderItem={({ item }) => (
            <View style={item.user ? styles.userMessage : styles.botMessage}>
              <Text style={item.user ? styles.userText : styles.botText}>
                {item.user || item.bot}
              </Text>
            </View>
          )}
          keyExtractor={(_, i) => i.toString()}
          contentContainerStyle={styles.messageList}
        />

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Type message..."
            value={input}
            onChangeText={setInput}
            editable={!loading}
          />
          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleSendMessage}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="white" />
            ) : (
              <Text style={styles.buttonText}>Send</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f7fafc' },
  messageList: { padding: 15 },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#667eea',
    borderRadius: 15,
    padding: 12,
    marginBottom: 10,
    maxWidth: '80%'
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#e2e8f0',
    borderRadius: 15,
    padding: 12,
    marginBottom: 10,
    maxWidth: '80%'
  },
  userText: { color: 'white', fontSize: 16 },
  botText: { color: '#2d3748', fontSize: 16 },
  inputContainer: {
    flexDirection: 'row',
    padding: 15,
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0'
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#e2e8f0',
    borderRadius: 8,
    padding: 12,
    marginRight: 10,
    fontSize: 16
  },
  button: {
    backgroundColor: '#667eea',
    borderRadius: 8,
    padding: 12,
    justifyContent: 'center',
    minWidth: 60
  },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: 'white', fontWeight: 'bold', textAlign: 'center' }
})
```

### Run on Device/Emulator

```bash
# iOS (Mac only)
expo run:ios

# Android
expo run:android

# Or use Expo Go app (easiest for testing)
expo start
# Scan QR code with Expo Go app (https://expo.dev/client)
```

---

## Option 2: Flutter (High Performance)

### Setup

```bash
# Install Flutter: https://flutter.dev/docs/get-started/install
flutter --version

# Create new app
flutter create chatbot_mobile
cd chatbot_mobile

# Add HTTP package
flutter pub add http uuid
```

### Main App (lib/main.dart)

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:uuid/uuid.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Chatbot',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map> messages = [];
  bool loading = false;
  final userId = const Uuid().v4();
  final conversationId = const Uuid().v4();

  final String apiUrl = 'http://YOUR_BACKEND_IP:8000';

  void sendMessage() async {
    if (_controller.text.isEmpty) return;

    setState(() {
      messages.add({'user': _controller.text});
      loading = true;
    });

    try {
      final response = await http.post(
        Uri.parse('$apiUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'text': _controller.text,
          'user_id': userId,
          'conversation_id': conversationId
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          messages.add({'bot': data['response']});
        });
      }
    } catch (e) {
      setState(() {
        messages.add({'bot': 'Error: $e'});
      });
    } finally {
      _controller.clear();
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Chatbot')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final msg = messages[index];
                final isUser = msg.containsKey('user');
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: EdgeInsets.all(8),
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.blue : Colors.grey[300],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      isUser ? msg['user'] : msg['bot'],
                      style: TextStyle(
                        color: isUser ? Colors.white : Colors.black,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Type message...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: loading ? null : sendMessage,
                  child: loading
                      ? CircularProgressIndicator(color: Colors.white)
                      : Icon(Icons.send),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Run

```bash
# iOS
flutter run -d iphone

# Android
flutter run -d android

# Web
flutter run -d chrome
```

---

## Option 3: Native Swift (iOS Only)

### Setup

```bash
# Create Swift project in Xcode
# File → New → Project → App
```

### Main View (ContentView.swift)

```swift
import SwiftUI

struct ContentView: View {
    @State var messages: [Message] = []
    @State var input = ""
    @State var loading = false

    let apiURL = "http://YOUR_BACKEND_IP:8000"

    func sendMessage() {
        guard !input.isEmpty else { return }

        messages.append(Message(role: "user", content: input))
        let userInput = input
        input = ""
        loading = true

        let payload = [
            "text": userInput,
            "user_id": "ios_user",
            "conversation_id": "conv_1"
        ] as [String: Any]

        guard let jsonData = try? JSONSerialization.data(withJSONObject: payload) else { return }

        var request = URLRequest(url: URL(string: "\(apiURL)/chat")!)
        request.httpMethod = "POST"
        request.httpBody = jsonData
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data,
               let json = try? JSONDecoder().decode(ChatResponse.self, from: data) {
                DispatchQueue.main.async {
                    messages.append(Message(role: "assistant", content: json.response))
                    loading = false
                }
            }
        }.resume()
    }

    var body: some View {
        VStack {
            ScrollView {
                VStack(spacing: 12) {
                    ForEach(messages) { message in
                        HStack {
                            if message.role == "user" { Spacer() }
                            Text(message.content)
                                .padding()
                                .background(message.role == "user" ? Color.blue : Color.gray)
                                .foregroundColor(.white)
                                .cornerRadius(12)
                            if message.role == "assistant" { Spacer() }
                        }
                    }
                }
                .padding()
            }

            HStack {
                TextField("Type message...", text: $input)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .disabled(loading)

                Button(action: sendMessage) {
                    if loading {
                        ProgressView()
                    } else {
                        Image(systemName: "paperplane.fill")
                    }
                }
                .disabled(loading || input.isEmpty)
            }
            .padding()
        }
    }
}

struct Message: Identifiable {
    let id = UUID()
    let role: String
    let content: String
}

struct ChatResponse: Codable {
    let response: String
}
```

---

## Option 4: Capacitor (React → iOS/Android)

### Setup

```bash
cd frontend

# Install Capacitor
npm install @capacitor/core @capacitor/cli

# Initialize
npx cap init

# Add platforms
npx cap add ios
npx cap add android

# Install plugins
npm install @capacitor/network
```

### Build & Deploy

```bash
# Build React app first
npm run build

# Sync to iOS/Android
npx cap sync

# Open in Xcode/Android Studio
npx cap open ios
npx cap open android
```

---

## Network Configuration

**Important:** For mobile to connect to backend:

### If Backend on Desktop:

```javascript
// Find your PC IP
// Windows/Mac: ifconfig | grep "inet "
// Use IP instead of localhost

const API_BASE_URL = 'http://192.168.1.100:8000'  // Your PC IP
```

### If Backend on Cloud:

```javascript
const API_BASE_URL = 'https://your-deployed-api.com'
```

### If Backend on Same Network:

```javascript
// Great! Just use PC IP
const API_BASE_URL = 'http://192.168.1.100:8000'
```

---

## Publishing to App Stores

### iOS (App Store)

```bash
# Build release
xcode build release

# Upload with Transporter app
# Follow: https://developer.apple.com/
```

### Android (Play Store)

```bash
# Generate signed APK
flutter build apk --release

# Upload to Google Play Console
# Follow: https://play.google.com/console
```

---

## Comparison

| Platform | Difficulty | Performance | Code Sharing |
|----------|-----------|-------------|--------------|
| React Native | Easy | Good | 80% |
| Flutter | Medium | Excellent | 0% |
| Swift | Hard | Excellent | 0% |
| Capacitor | Easy | Good | 95% |

**Recommendation:** Start with **React Native/Expo** for fastest development.

---

## Testing

```bash
# React Native
npm test

# Flutter
flutter test

# Swift
xcodebuild test

# Web (same frontend)
npm run test
```

---

## Common Issues

**"Cannot connect to backend"**
- Use PC IP, not localhost
- Check firewall allows port 8000
- Backend must be running

**"Module not found"**
```bash
npm install
flutter pub get
```

**"Build fails"**
- Clean build: `flutter clean`
- Reinstall: `npm install`
- Update Xcode/Android Studio

---

Enjoy your mobile app! 🚀
