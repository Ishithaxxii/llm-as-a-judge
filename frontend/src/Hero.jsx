import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
// import NeuralNetwork from "./NeuralNetwork";
import FloatingConsensus from "./FloatingConsensus";

const stats = [
  {
    value: "4+",
    label: "AI Judges",
  },
  {
    value: "15+",
    label: "Evaluation Metrics",
  },
  {
    value: "99%",
    label: "Consensus Accuracy",
  },
];

export default function Hero() {
  return (
    <section className="relative overflow-hidden px-6 pt-28 pb-24">
      <div className="mx-auto grid max-w-7xl items-center gap-20 lg:grid-cols-2">
        {/* LEFT SIDE */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-2">
            <Sparkles size={16} className="text-primary" />

            <span className="text-sm font-medium text-primary">
              Multi-Agent Consensus Intelligence
            </span>
          </div>

          <h1 className="font-heading text-5xl font-bold leading-tight text-white md:text-7xl">
            AI judges.
            <br />
            <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
              One trusted verdict.
            </span>
          </h1>

          <p className="mt-8 max-w-xl text-lg leading-8 text-muted md:text-xl">
            Evaluate code, essays, research papers, and free-form text using
            multiple independent AI models. Compare their reasoning, measure
            agreement, and generate a transparent consensus score.
          </p>

          <div className="mt-12 flex flex-wrap gap-5">
            <a
              href="#workspace"
              className="group inline-flex items-center gap-2 rounded-full bg-primary px-8 py-4 font-semibold text-white transition hover:scale-105 hover:bg-secondary"
            >
              Start Evaluation

              <ArrowRight
                size={18}
                className="transition group-hover:translate-x-1"
              />
            </a>

            <a
              href="#features"
              className="rounded-full border border-white/10 px-8 py-4 text-white transition hover:border-primary hover:bg-white/5"
            >
              Learn More
            </a>
          </div>

          <div className="mt-16 grid grid-cols-3 gap-4">
            {stats.map((item) => (
              <motion.div
                whileHover={{ y: -6 }}
                key={item.label}
                className="rounded-3xl border border-white/10 bg-card/60 p-6 backdrop-blur-xl"
              >
                <h3 className="font-heading text-3xl font-bold text-white">
                  {item.value}
                </h3>

                <p className="mt-2 text-sm text-muted">
                  {item.label}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* RIGHT SIDE */}
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{
                duration: 1,
                delay: 0.3,
            }}
            className="hidden items-center justify-center lg:flex"
            >
            <FloatingConsensus />
        </motion.div>
      </div>
    </section>
  );
}