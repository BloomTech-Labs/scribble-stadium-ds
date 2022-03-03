import clustering_mvp
import unittest

cohort = {"01": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 68, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "02": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 94, "Skipped": True, "Pages": {"1": "sample", "2": "sample"}},
          "03": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 21, "Skipped": True, "Pages": {"1": "sample", "2": "sample"}},
          "04": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 75, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "05": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 45, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "06": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 57, "Skipped": True, "Pages": {"1": "sample", "2": "sample"}},
          "07": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 62, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "08": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 53, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "09": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 85, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "10": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 72, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "11": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 89, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}},
          "12": {"Image": "sample", "Inappropriate": False, "Sensitive": False, "Status": "APPROVED",
                 "Complexity": 49, "Skipped": False, "Pages": {"1": "sample", "2": "sample"}}
          }

result = clustering_mvp.cluster(cohort)

print(result)
