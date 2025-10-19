import { useEffect, useRef } from "react";
import { FileText, Zap, Shield, MessageSquare, Brain, Lock } from "lucide-react";

const features = [
  {
    icon: FileText,
    title: "PDF Intelligence",
    description: "Upload any PDF document and instantly unlock its knowledge with AI-powered analysis.",
  },
  {
    icon: MessageSquare,
    title: "Natural Conversations",
    description: "Ask questions in plain language and receive precise, context-aware answers.",
  },
  {
    icon: Brain,
    title: "Deep Understanding",
    description: "Advanced AI comprehends complex documents, extracting insights beyond simple keyword searches.",
  },
  {
    icon: Zap,
    title: "Instant Results",
    description: "Get answers in seconds, not minutes. Lightning-fast processing for immediate insights.",
  },
  {
    icon: Shield,
    title: "Privacy First",
    description: "Your documents stay secure. End-to-end encryption ensures complete data protection.",
  },
  {
    icon: Lock,
    title: "Enterprise Security",
    description: "Bank-level security standards with compliance-ready infrastructure.",
  },
];

const Features = () => {
  const featuresRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const cards = entry.target.querySelectorAll('.feature-card');
            cards.forEach((card, index) => {
              setTimeout(() => {
                card.classList.add('animate-slide-up');
              }, index * 100);
            });
          }
        });
      },
      { threshold: 0.1 }
    );

    if (featuresRef.current) {
      observer.observe(featuresRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section ref={featuresRef} className="py-24 px-4 relative">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold">
            Powerful <span className="text-gradient">Features</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Everything you need to transform static documents into dynamic, queryable knowledge bases.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="feature-card glass-card p-8 rounded-2xl opacity-0 hover:scale-105 transition-transform duration-300 group"
            >
              <div className="mb-6 inline-flex items-center justify-center w-14 h-14 rounded-xl bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors duration-300">
                <feature.icon className="h-7 w-7" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
