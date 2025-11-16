# Cybernetic VSM - Viable System Model Pipeline

A production-ready React + TypeScript application implementing the VSM (Viable System Model) cybernetic hierarchy for intelligent task orchestration using AI agents through OpenRouter.ai.

## Overview

This application provides a visual interface for the VSM hierarchy pipeline, featuring 4 specialized AI agents working together to analyze, plan, and execute complex tasks:

- **Policy Agent (System 5)** - Governance & Ethics
- **Intelligence Agent (System 4)** - Strategic Planning
- **Control Agent (System 3)** - Execution Management
- **Coordination Agent (System 2)** - Conflict Prevention

## Features

- ✅ **NSL Brand Theme** - Dark purple/golden themed UI with elegant animations
- ✅ **OpenRouter.ai Integration** - Flexible LLM provider with model selection
- ✅ **Browser Storage** - Persistent user preferences (API key, model)
- ✅ **Real-time Progress** - Live execution tracking with agent visualization
- ✅ **VSM Pipeline** - Complete cybernetic hierarchy implementation
- ✅ **Responsive Design** - Mobile-first with TailwindCSS
- ✅ **FontAwesome Icons** - Professional icon library integration

## Tech Stack

- **React 19** - Modern UI framework
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **FontAwesome** - Icon library
- **OpenRouter.ai** - Multi-model LLM gateway

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cybernetic-vsm-app
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to the URL shown (typically `http://localhost:5173`)

## Configuration

### OpenRouter API Key

1. Click the **Settings** icon (⚙️) in the top-right corner
2. Enter your OpenRouter API key from [openrouter.ai/keys](https://openrouter.ai/keys)
3. Optionally change the model (default: `x-ai/grok-beta`)
4. Click **Save Settings**

Your settings are stored in browser localStorage and persist across sessions.

### Supported Models

Any model available on OpenRouter.ai can be used. Popular options:

- `x-ai/grok-beta` (default) - Fast and intelligent
- `anthropic/claude-3-opus` - Most capable
- `anthropic/claude-3-sonnet` - Balanced performance
- `openai/gpt-4-turbo` - OpenAI's latest
- `google/gemini-pro` - Google's model

See all available models at [openrouter.ai/models](https://openrouter.ai/models)

## Usage

1. **Enter a task** in the Task Input textarea
2. **Click "Execute Task"** to start the VSM pipeline
3. **Watch the agents work** in real-time:
   - Intelligence Agent creates a strategic plan
   - Policy Agent validates compliance
   - Coordination Agent plans resources
   - Control Agent simulates execution
   - Policy Agent provides final validation
4. **View results** in the Agent Messages panel

### Example Tasks

- "Create a comprehensive tutorial on Python async/await"
- "Analyze the pros and cons of different database architectures"
- "Plan a marketing strategy for a new SaaS product"
- "Design a RESTful API for a task management system"

## VSM Hierarchy Flow

```
User Task
    ↓
Intelligence Agent (System 4)
    ↓ [Strategic Plan]
Policy Agent (System 5)
    ↓ [Compliance Check]
Coordination Agent (System 2)
    ↓ [Resource Planning]
Control Agent (System 3)
    ↓ [Execution Simulation]
Policy Agent (System 5)
    ↓ [Final Validation]
Result
```

## Project Structure

```
cybernetic-vsm-app/
├── src/
│   ├── components/
│   │   ├── AgentMessage.tsx      # Agent message display
│   │   ├── SettingsModal.tsx     # Settings configuration
│   │   └── VSMDiagram.tsx        # VSM hierarchy visualization
│   ├── types/
│   │   └── index.ts              # TypeScript type definitions
│   ├── utils/
│   │   ├── openrouter.ts         # OpenRouter API client
│   │   ├── storage.ts            # Browser storage utilities
│   │   └── vsmPipeline.ts        # VSM pipeline orchestration
│   ├── App.tsx                   # Main application component
│   ├── index.css                 # Global styles + NSL theme
│   └── main.tsx                  # Application entry point
├── public/                       # Static assets
├── index.html                    # HTML template
├── package.json                  # Dependencies
├── tailwind.config.js           # TailwindCSS configuration
├── tsconfig.json                # TypeScript configuration
└── vite.config.ts               # Vite configuration
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Building for Production

```bash
npm run build
```

Output will be in the `dist/` directory, ready to deploy to any static hosting service.

## NSL Brand Styling

The application follows the NSL brand style guidance with:

- **Color Palette**: Dark purple primary, golden accent
- **Typography**: Semantic heading hierarchy
- **Animations**: Smooth transitions and effects
- **Shadows**: Elegant depth and glow effects
- **Accessibility**: WCAG AA compliant contrast ratios

## Architecture

### VSM Pipeline

The pipeline implements cybernetic control principles:

1. **Requisite Variety** - Each agent matches complexity to responsibility
2. **Feedback Loops** - Quality gates and refinement cycles
3. **Homeostasis** - Self-regulating quality thresholds
4. **Algedonic Signals** - Rapid escalation for critical issues

### Agent Communication

Agents communicate through structured prompts:
- System prompt defines agent role and responsibilities
- User prompt provides task context
- Responses are captured and displayed in real-time

## Credits

Based on the [Cognition-9](https://github.com/MushroomFleet/Cognition-9) multi-agent orchestration system implementing Stafford Beer's Viable System Model.

## License

Research project - See main Cognition-9 repository for license details.

## Support

For issues or questions:
- Check the [Cognition-9 documentation](https://github.com/MushroomFleet/Cognition-9)
- Review OpenRouter.ai [documentation](https://openrouter.ai/docs)
- Open an issue on GitHub
