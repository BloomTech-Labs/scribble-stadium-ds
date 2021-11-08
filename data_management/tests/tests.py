import unittest
import warnings
from PIL import ImageFile
from data_management.management_utils import management_utils


class PipeLinePhases(unittest.TestCase):
    def test_basic_properties(self):
        from data_management.story_photo_transformer import phase_list

        for i, cls in enumerate(phase_list):
            print(cls)
            a = cls(None)

            self.assertTrue("phase" in a.__dir__(),
                            "no phase name in " + str(cls) + " phase should be = phase" + str(i),
            )


class TestCpuLoader(unittest.TestCase):

    def test_data_path(self):
        import os
        cdl = management_utils.CPUDataLoader()

        def check_path():
            os.path.exists(cdl.data_path)
        self.assertTrue(check_path(), "expected data directory does not exist: " + cdl.data_path)

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

        # Test stories are readable in utf8, this should throw an error if encountering binary file,
        # exceptions need researched
        for fname in storys:
            try:
                with open(fname, encoding="utf8") as file:
                    file.readlines()
            except Exception as e:
                errors.append("error in transcription: " + fname +" "+str(e))
        self.assertTrue(errors == [], "\n".join(errors))

        # test that all images are loadable
        found_names = []
        for fname in storys:
            story_name = fname
            fname = fname.replace("Story", "Photo")
            page_types = ["", " pg1", " pg2", " pg3"]
            extensions = [".jpg", ".tif", ",png"]
            image_names = [fname + pt + ex for ex in extensions for pt in page_types]

            # Some typos occurred during transcription, these patterns will generate a warning
            image_names_warning = [
                fname + " .jpg",
                fname + " pg1 .jpg",
                fname + " pg2 .jpg",
            ]

            image_names_to_check = image_names + image_names_warning

            found_valid = False
            found_name = None
            for image_name in image_names_to_check:
                if cv2.haveImageReader(image_name):
                    found_valid = True
                    found_name = image_name
                    found_names.append(found_name)
                else:
                    pass

            if not found_valid:
                errors.append("error in : " + story_name)

            if found_name in image_names_warning:
                with self.assertWarns(ResourceWarning):
                    warnings.simplefilter("always")
                    warnings.warn(
                        str(found_name)
                        + " has a file name format that is on the warning list",
                        ResourceWarning,
                    )
                    print(
                        str(found_name)
                        + " has a file name format that is on the warning list"
                    )

        # test that all images are of sufficient resolution
        sizes = set()
        for fname in found_names:
            with open(fname, "rb") as f:
                ImPar = ImageFile.Parser()
                chunk = f.read(2048)
                count = 2048
                while not ImPar.image:
                    ImPar.feed(chunk)
                    chunk = f.read(2048)
                    count += 2048
                sz = ImPar.image.size
                sz = list(sz)
                sz.sort()
                sizes.add((sz[1], sz[0]))

        print("found image sizes", sizes)
        for size in sizes:
            self.assertTrue((size[0] * size[1]) >= (640 * 480))


if __name__ == '__main__':
    unittest.main()
