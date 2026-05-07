#!/bin/bash
# Setup script for ASR Benchmark project

echo "=================================================="
echo "ASR Benchmark - Setup Instructions"
echo "=================================================="
echo ""

echo "✅ Step 1: Project structure created"
echo ""

echo "📋 Next steps:"
echo ""
echo "1. Copy your 20 audio files (.ogg) to:"
echo "   → data/audio/"
echo ""
echo "2. Install Python dependencies:"
echo "   → pip install -r requirements.txt"
echo ""
echo "3. Get API keys:"
echo "   → Deepgram: https://console.deepgram.com/"
echo "   → AssemblyAI: https://www.assemblyai.com/dashboard/"
echo ""
echo "4. Create .env file (copy from template):"
echo "   → cp .env.template .env"
echo "   → Edit .env and add your API keys"
echo ""
echo "5. Run the benchmark:"
echo "   → python src/benchmark.py"
echo ""
echo "=================================================="
echo ""

# Check current status
echo "Current status:"
echo "---------------"

if [ -f "data/labels/labels.csv" ]; then
    echo "✅ labels.csv found"
else
    echo "❌ labels.csv missing"
fi

AUDIO_COUNT=$(ls -1 data/audio/*.ogg 2>/dev/null | wc -l)
echo "📁 Audio files: $AUDIO_COUNT/20"

if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not created yet (copy from .env.template)"
fi

echo ""
