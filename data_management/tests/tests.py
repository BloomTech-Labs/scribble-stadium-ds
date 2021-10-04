import unittest
import warnings

from data_management.management_utils import management_utils


class PipeLinePhases(unittest.TestCase):
    def test_basic_properties(self):
        from data_management.story_photo_transformer import phase_list
        for i,cls in enumerate(phase_list):
            print(cls)
            a = cls(None)

            self.assertTrue("phase" in a.__dir__(),"no phase name in "+str(cls)+" phase should be = phase"+str(i))


class TestCpuLoader(unittest.TestCase):

    def test_data_path(self):
        import os
        cdl = management_utils.CPUDataLoader()

        f = lambda: os.path.exists(cdl.data_path)
        self.assertTrue(f(), "expected data directory does not exist: " + cdl.data_path)

    def test_data_file_structure(self):
        """
        expecting structure like:
        transcribed_stories
          31--
            3101
              photo 3101.jpg
              Story 3101
              *or*
              Photo 3101 pg1.jpg
              photo 3101 pg2.jpg
              story 3101
        ...
        """
        import glob
        import os
        import data_management.management_utils

        data_path = management_utils.CPUDataLoader().data_path
        storys = glob.glob(os.path.join(data_path, "*", "*", "Story*"))
        self.assertTrue(len(storys) > 3, "No storys found")

    def test_data_file_contents(self):
        """
        Tests the actual contents of the images and transcriptions
        """
        import glob
        import os
        import cv2
        cdl = management_utils.CPUDataLoader()

        errors = []
        data_path = cdl.data_path
        storys = glob.glob(os.path.join(data_path, "*", "*", "Story*"))

        # Test stories are readable in ut8, this should throw an error if encountering binary file,
        # exceptions need researched
        for fname in storys:
            try:
                with open(fname, encoding="utf8") as file:
                    file.readlines()
            except:
                errors.append("error in transcription: " + fname)

        self.assertTrue(errors == [], "\n".join(errors))

        # test that all images are loadable

        for fname in storys:
            story_name = fname
            fname = fname.replace("Story", "Photo")
            image_names = [fname + ".jpg", fname + " pg1.jpg", fname + " pg2.jpg"]

            # Some typos occured during transcription, these patterns will generate a warning
            image_names_warning = [fname + " .jpg", fname + " pg1 .jpg", fname + " pg2 .jpg"]

            image_names_to_check = image_names + image_names_warning

            found_valid = False
            for image_name in image_names_to_check:
                if cv2.haveImageReader(image_name):
                    found_valid = True
                    found_name = image_name
                else:
                    pass

            if not found_valid:
                errors.append("error in : " + story_name)

            if found_name in image_names_warning:
                with self.assertWarns(UserWarning) as cm:
                    warnings.warn(cm)
                    print(found_name + " has a file name format that is on the warning list")


if __name__ == '__main__':
    unittest.main()
