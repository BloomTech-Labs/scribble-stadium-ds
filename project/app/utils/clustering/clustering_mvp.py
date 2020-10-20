import json

import pandas as pd


def cluster(cohort_submissions: dict) -> list:
    """
    Splits given dict into clusters of 4 based on their ranked complexity

    The 'remainder problem' of needing to have 4 submissions per cluster,
    regardless of number of submissions, is solved here by duplicating
    submission IDs across clusters to supplement any clusters with less than 4,
    with no clusters containing more than 1 submission_ID that also
    appears in another cluster, unless there are fewer than 3 total
    submissions, or exactly 5 submissions, in the given cohort.

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
    num_clusters = num_submissions // 4
    remainder = num_submissions % 4
    clusters = []

    # Edge Cases:
    # - less than 4, they are all in one group
    if num_submissions < 4:
        return "Not enough submissions in this cohort to form a full cluster"

    # If the remainder is 3 -> last group will be a group of 3 users
    elif remainder == 3:
        # Cluster submissions until 7 remain
        for i in range(num_clusters - 1):
            # Group by top 4 squad scores
            clusters.append(list(df.index[:4]))
            # Drop stories you have grouped already
            df = df[4:]

        # Manually cluster final two groups to handle remainder problem
        # by duplicating 1 submission so each have 4 submission_ids
        clusters.append(list(df.index[:4]))
        clusters.append(list(df.index[3:]))

    # If the remainder is 2 -> last 2 groups will be groups of 3
    elif remainder == 2:
        if num_submissions == 6:
            clusters.append(list(df.index[:4]))
            clusters.append(list(df.index[2:]))
        else:
            # Cluster submissions until 10 remain
            for i in range(num_clusters - 2):
                # Group by top 4 squad scores
                clusters.append(list(df.index[:4]))
                # Drop stories you have grouped already
                df = df[4:]

            # Manually cluster final three groups to handle remainder problem
            clusters.append(list(df.index[:4]))
            clusters.append(list(df.index[3:7]))
            clusters.append(list(df.index[6:]))

    # If the remainder is 1 -> last 3 groups will be groups of 3
    elif remainder == 1:
        if num_submissions == 5:
            # Overlap both clusters by 3 submissions
            clusters.append(list(df.index[:4]))
            clusters.append(list(df.index[1:]))
        elif num_submissions == 9:
            clusters.append(list(df.index[:4]))
            clusters.append(list(df.index[2:6]))
            clusters.append(list(df.index[5:]))
        else:
            # Cluster submissions until 13 remain
            for i in range(num_clusters - 3):
                # Group by top 4 squad scores
                clusters.append(list(df.index[:4]))
                # Drop stories you have already grouped
                df = df[4:]

            # Manually cluster final three overlapping groups to handle
            # remainder problem
            clusters.append(list(df.index[:4]))
            clusters.append(list(df.index[3:7]))
            clusters.append(list(df.index[6:10]))
            clusters.append(list(df.index[9:]))

    # Else, the remainder is 0. Split evenly by 4
    else:
        for i in range(num_clusters):
            # Group by top 4 squad scores
            clusters.append(list(df.index[:4]))
            # Drop stories you have already grouped
            df = df[4:]

    return clusters


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
