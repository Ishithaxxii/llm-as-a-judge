import { motion } from "framer-motion";

const particles = Array.from({ length: 45 }, (_, i) => ({
  id: i,
  left: Math.random() * 100,
  top: Math.random() * 100,
  size: 2 + Math.random() * 4,
  duration: 8 + Math.random() * 8,
  delay: Math.random() * 5,
}));

export default function CosmicBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">

      {/* Animated Gradient */}
      <motion.div
        animate={{
          backgroundPosition: [
            "0% 50%",
            "100% 50%",
            "0% 50%",
          ],
        }}
        transition={{
          duration: 35,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute inset-0"
        style={{
          background: `
            radial-gradient(circle at 20% 20%, rgba(124,92,252,.18), transparent 35%),
            radial-gradient(circle at 80% 25%, rgba(0,212,255,.14), transparent 30%),
            radial-gradient(circle at 50% 85%, rgba(59,130,246,.16), transparent 35%),
            #060816
          `,
          backgroundSize: "200% 200%",
        }}
      />

      {/* Purple Blob */}
      <motion.div
        animate={{
          x: [0, 60, 0],
          y: [0, -40, 0],
        }}
        transition={{
          duration: 24,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute left-[-150px] top-[120px] h-[500px] w-[500px] rounded-full bg-primary/10 blur-[130px]"
      />

      {/* Cyan Blob */}
      <motion.div
        animate={{
          x: [0, -50, 0],
          y: [0, 30, 0],
        }}
        transition={{
          duration: 28,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute right-[-180px] bottom-[100px] h-[420px] w-[420px] rounded-full bg-accent/10 blur-[130px]"
      />

      {/* Floating Particles */}
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          animate={{
            y: [0, -25, 0],
            opacity: [0.2, 0.8, 0.2],
          }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute rounded-full bg-white/40"
          style={{
            width: particle.size,
            height: particle.size,
            left: `${particle.left}%`,
            top: `${particle.top}%`,
          }}
        />
      ))}
    </div>
  );
}