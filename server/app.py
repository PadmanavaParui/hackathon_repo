import uvicorn

def main():
    # Points the openenv validator back to our working main.py file
    uvicorn.run("main:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()