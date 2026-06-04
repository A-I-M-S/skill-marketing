module.exports = {
  apps: [
    {
      name: "skill-marketing",
      script: "tools/marketing-daemon",
      cwd: "/home/openclaw/skill-marketing",
      interpreter: "bash",
      autorestart: true,
      watch: false,
      max_memory_restart: "200M",
      out_file: "logs/pm2-out.log",
      error_file: "logs/pm2-error.log",
      merge_logs: true,
      env: {
        MARKETING_LOG_FILE: "logs/marketing-combined.log"
      }
    }
  ]
};
