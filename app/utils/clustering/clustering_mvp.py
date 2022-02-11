import json

import pandas as pd


def cluster(cohort_submissions: dict) -> list:
    """
    Naming structure for variables:
    team = 2 players (1 submission each)
    squad = 2 Teams
    cohort = group of squads
    """
    """
    Splits given dict into groups of 4 based on their ranked complexity

    Input: dictionary of a single cohort containing nested dictionary
    with 'submission_id' as first level key,
    and 'complexity' as one of the inner keys
    Output: Nested list of clusters:
    [[list of submission_ids], [list of submission_ids]]
    """

    # Generate DataFrame from dict
    df = pd.DataFrame.from_dict(cohort_submissions, orient="index")

    # Rank by complexity
    df = df.sort_values(by=["Complexity"], ascending=False)

    # Initial variables
    num_submissions = len(df)
    remainder = num_submissions % 4
    matching_minimum = 8

    # assuming cohorts are divisible by 4, then squads can be returned like this.
    if remainder == 0 and num_submissions >= matching_minimum:
        return [df[i:i+4] for i in range(0, len(df), 4)]

    else:
        return "Cohort not ready for matching"


async def batch_cluster(submissions: dict) -> json:
    """
    Generates a return JSON object of clusters for all provided cohorts.

    Input: dictionary of all cohort submissions
    Output: JSON object of nested lists of submission IDs by cluster, by cohort

    To test locally in isolation as an async function, run the following code:
    import asyncio
    asyncio.run(batch_cluster(submissions_json))
    """

    # Initiate cluster dictionary
    cluster_dict = {}

    # Iterate through cohorts to get clusters, and
    # add each to cluster_dict
    for cohort_id in submissions:
        clusters = cluster(submissions[cohort_id])
        cluster_dict[cohort_id] = clusters

    # Convert dict back to JSON
    cluster_json = json.dumps(cluster_dict)

    return cluster_json
