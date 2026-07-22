*Welcome to my spoilage and quality automation practice project*

---------

The intention of this project is to know more about claude code usage, AI agents and automated n8n workflows. Made by Juan Camilo Cardenas Zabala.

-----

**SYSTEM DIAGRAM:**
![System diagram](system-diagram.png)

------
**HOW TO RUN THE PROJECT:**

1. Make sure to run in your console:
```
docker compose up -d.
```

2. After that run:
```
python3.12 simulators/batch_simulator.py
```
3. Check the resulting data in `data/generated_batches.json`
