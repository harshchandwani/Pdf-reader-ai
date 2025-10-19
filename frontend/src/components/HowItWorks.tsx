import { useEffect, useRef } from "react";
import { Upload, Sparkles, MessageCircle } from "lucide-react";

const steps = [
  {
    icon: Upload,
    step: "01",
    title: "Upload Your PDF",
    description: "Simply drag and drop or select your PDF document. Any size, any complexity.",
  },
  {
    icon: Sparkles,
    step: "02",
    title: "AI Processing",
    description: "Our advanced AI analyzes your document, understanding context, structure, and content.",
  },
  {
    icon: MessageCircle,
    step: "03",
    title: "Ask & Discover",
    description: "Start asking questions naturally. Get precise answers with exact references to your document.",
  },
];

const HowItWorks = () => {
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const steps = entry.target.querySelectorAll('.step-card');
            steps.forEach((step, index) => {
              setTimeout(() => {
                step.classList.add('animate-scale-in');
              }, index * 200);
            });
          }
        });
      },
      { threshold: 0.1 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} className="py-24 px-4 bg-card/30">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold">
            How It <span className="text-gradient">Works</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Three simple steps to unlock the power of your documents
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Connection lines (hidden on mobile) */}
          <div className="hidden md:block absolute top-24 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-primary via-purple-500 to-primary" />
          
          {steps.map((stepItem, index) => (
            <div
              key={index}
              className="step-card opacity-0 relative"
            >
              <div className="glass-card p-8 rounded-2xl text-center space-y-6 hover:border-primary/50 transition-all duration-300">
                {/* Step number */}
                <div className="absolute -top-4 -right-4 w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm">
                  {stepItem.step}
                </div>
                
                {/* Icon */}
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-purple-500 text-white animate-glow-pulse">
                  <stepItem.icon className="h-10 w-10" />
                </div>

                {/* Content */}
                <div className="space-y-3">
                  <h3 className="text-2xl font-semibold">{stepItem.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {stepItem.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
