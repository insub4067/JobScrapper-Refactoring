from db import db
import asyncio
from functions.stackOverflow import *
from functions.remotely import *
from functions.remoteok import *
import time


# SCRAP SPREADER
def scrap_jobs(word):

    start = time.time()

    stackOverflow_jobs = asyncio.run(scrap_stackOverflow(word))
    remotely_jobs = asyncio.run(scrap_remotely(word))
    remoteok_jobs = asyncio.run(scrap_remoteok(word))
    jobs = stackOverflow_jobs + remotely_jobs + remoteok_jobs
    db[word] = jobs

    end = time.time()

    print("SCRAP RUNTIME : ", end - start)

    return jobs
