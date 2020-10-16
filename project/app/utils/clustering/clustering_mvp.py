import json

import pandas as pd


def cluster(cohort_submissions: dict) -> list:
    '''
    Splits given dict into clusters of 4 based on their ranked complexity

    When there is a remainder of users not evenly divisible by 4,
    remainder is split so there is never more than 1 computer user in a group,
    unless there are fewer than 3 users.

    Input: dictionary of a single cohort containing nested dictionary
    with 'submission_id' as first level key,
    and 'complexity' as one of the inner keys
    Output: Nested list of clusters:
    [[list of submission_ids], [list of submission_ids]]
    '''

    # Generate DataFrame from dict
    df = pd.DataFrame.from_dict(cohort_submissions, orient='index')

    # Rank by complexity
    df = df.sort_values(by=['complexity'], ascending=False)

    # Initial variables
    num_submissions = len(df)
    num_clusters = num_submissions // 4
    remainder = num_submissions % 4
    clusters = []

    # Edge Cases:
    # - less than 4, they are all in one group
    # - 5, one group of 3 one group of 2
    if num_submissions < 4:
        clusters.append(list(df.index[:]))
        return clusters

    elif num_submissions == 5:
        clusters.append(list(df.index[:3]))
        clusters.append(list(df.index[3:]))
        return clusters

    # If the remainder is 3 -> last group will be a group of 3 users
    if remainder == 3:
        for i in range(num_clusters):
            # Group by top 4 squad scores
            clusters.append(list(df.index[:4]))
            # Drop stories you have grouped already
            df = df[4:]

        # Final group is the last 3 remainders
        clusters.append(list(df.index[:]))
        return clusters

    # If the remainder is 2 -> last 2 groups will be groups of 3
    elif remainder == 2:
        # Leave the last 2 groups to split into 2 groups of 3
        for i in range(num_clusters - 1):
            # Group by top 4 squad scores
            clusters.append(list(df.index[:4]))
            # Drop stories you have grouped already
            df = df[4:]

        # The last two groups will be groups of 3
        clusters.append(list(df.index[:3]))
        clusters.append(list(df.index[3:]))
        return clusters

    # If the remainder is 1 -> last 3 groups will be groups of 3
    elif remainder == 1:
        # Leave the last 3 groups to be split into 3 groups of 3
        for i in range(num_clusters - 2):
            # Group by top 4 squad scores
            clusters.append(list(df.index[:4]))
            # Drop stories you have already grouped
            df = df[4:]

        # The last three groups as groups of 3
        clusters.append(list(df.index[:3]))
        clusters.append(list(df.index[3:6]))
        clusters.append(list(df.index[6:]))
        return clusters

    # Else, the remainder is 0. Split evenly by 4
    else:
        for i in range(num_clusters):
            # Group by top 4 squad scores
            clusters.append(list(df.index[:4]))
            # Drop stories you have already grouped
            df = df[4:]
        return clusters


async def batch_cluster(submissions_json: json) -> json:
    """
    Generates a return JSON object of clusters for all provided cohorts.

    Input: JSON object of all cohort submissions
    Output: JSON object of nested lists of submission IDs by cluster, by cohort

    To test locally in isolation as an async function, run the following code:
    import asyncio
    asyncio.run(batch_cluster(submissions_json))
    """

    # Convert JSON to dictionary
    submissions = json.loads(submissions_json)

    # Initiate cluster dictionary
    cluster_dict = {}

    # Iterate through cohorts to get clusters, and
    # add each to cluster_dict
    for cohort_id in submissions.keys():
        clusters = cluster(submissions[cohort_id])
        cluster_dict[cohort_id] = clusters

    # Convert dict back to JSON
    cluster_json = json.dumps(cluster_dict)

    return cluster_json
