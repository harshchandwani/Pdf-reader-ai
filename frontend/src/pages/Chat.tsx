// filepath: /Users/harshchandwani/Projects/Pdf-reader-ai/frontend/src/pages/Chat.tsx
import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";
import { ArrowLeft, Send, Upload, FileText } from "lucide-react";

const Chat = () => {
  const [messages, setMessages] = useState<
    Array<{ role: "user" | "assistant"; content: string }>
  >([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Ref for auto-scroll
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // Scroll to bottom on message change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async () => {
    const question = inputMessage.trim();
    if (!question || isLoading) return;

    // Add user message + temporary assistant message
    setMessages((prev) => [
      ...prev,
      { role: "user", content: question },
      { role: "assistant", content: "..." }, // temporary placeholder
    ]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const session_id = sessionStorage.getItem("session_id");
      if (!session_id) {
        throw new Error("No session_id found in sessionStorage");
      }

      const API_URL = import.meta.env.VITE_API_URL;
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id,
          question,
        }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      // Determine reply text
      const assistantReply =
        data.answer ||
        data.reply ||
        data.response ||
        (typeof data === "string" ? data : JSON.stringify(data));

      // Replace the temporary "..." message with the real response
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: "assistant",
          content: assistantReply,
        };
        return newMessages;
      });
    } catch (error) {
      console.error("Error fetching AI response:", error);
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: "assistant",
          content: "Sorry, I couldn't get a response. Please try again.",
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b border-border/50 backdrop-blur-xl bg-card/30 sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <FileText className="h-5 w-5 text-primary" />
              </div>
              <div>
                <h1 className="text-lg font-semibold">Document.pdf</h1>
                <p className="text-xs text-muted-foreground">Ready to query</p>
              </div>
            </div>
          </div>

          <Link to="/upload">
            <Button variant="glass" size="sm">
              <Upload className="h-4 w-4 mr-2" />
              Upload New
            </Button>
          </Link>
        </div>
      </header>

      {/* Chat Messages */}
      <main className="flex-1 overflow-y-auto">
        <div className="container mx-auto max-w-4xl px-4 py-8">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-6">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-purple-500 flex items-center justify-center animate-glow-pulse">
                <FileText className="h-10 w-10 text-white" />
              </div>
              <div className="text-center space-y-2">
                <h2 className="text-2xl font-bold">
                  Ask anything about your document
                </h2>
                <p className="text-muted-foreground max-w-md">
                  Start a conversation with your PDF. Ask questions, request
                  summaries, or extract specific information.
                </p>
              </div>
              <div className="flex flex-wrap gap-2 justify-center max-w-2xl">
                <Button
                  variant="glass"
                  size="sm"
                  onClick={() =>
                    setInputMessage("What is this document about?")
                  }
                >
                  What is this document about?
                </Button>
                <Button
                  variant="glass"
                  size="sm"
                  onClick={() =>
                    setInputMessage("Summarize the main points")
                  }
                >
                  Summarize the main points
                </Button>
                <Button
                  variant="glass"
                  size="sm"
                  onClick={() =>
                    setInputMessage("Extract key information")
                  }
                >
                  Extract key information
                </Button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  } animate-slide-up`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-6 py-4 ${
                      message.role === "user"
                        ? "bg-primary text-primary-foreground ml-auto"
                        : "glass-card"
                    }`}
                  >
                    <p className="text-sm leading-relaxed">
                      {message.content === "..."
                        ? "Thinking..."
                        : message.content}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>
          )}
        </div>
      </main>

      {/* Input */}
      <footer className="border-t border-border/50 backdrop-blur-xl bg-card/30 sticky bottom-0">
        <div className="container mx-auto max-w-4xl px-4 py-4">
          <div className="flex gap-3">
            <Input
              placeholder="Ask a question about your document..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
              className="flex-1 bg-background/50 border-border/50 focus-visible:ring-primary"
            />
            <Button
              variant="hero"
              size="icon"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
          <p className="text-xs text-muted-foreground text-center mt-2">
            DocuQuery uses AI to analyze your documents. Responses may vary.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Chat;
