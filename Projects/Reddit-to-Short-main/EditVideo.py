import os
import shutil
import logging
from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx
from skimage.filters import gaussian
import config

debug = config.debug


def configure_logging():
    """Configure logging level based on the debug flag."""
    if debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Render:
    def __init__(self, directory, clip_name, output_name, resolution):
        """
        Initializes the Render object with directory, clip name, output name, and resolution.

        Args:
            directory (str): The directory where the video files are located.
            clip_name (str): The name of the input video clip.
            output_name (str): The name of the output video clip.
            resolution (tuple): The desired resolution for the output video.
        """
        self.directory = directory
        self.clip_name = clip_name
        self.output_name = output_name
        self.resolution = resolution

    @staticmethod
    def blur(image):
        """
        Applies a Gaussian blur to the image.

        Args:
            image (ndarray): The image to be blurred.

        Returns:
            ndarray: The blurred image.
        """
        return gaussian(image.astype(float), sigma=25)

    @property
    def render(self):
        """
        Resizes, centers, and renders a video clip with optional edge blur if needed.

        Returns:
            bool: True if the rendering is successful, False otherwise.
        """
        try:
            input_path = os.path.join(self.directory, self.clip_name)
            output_path = os.path.join(self.directory, self.output_name)

            if self.resolution is None:
                logging.debug("No resolution set, copying the input clip to the output.")
                shutil.copy(input_path, output_path)
                return True

            main_clip = VideoFileClip(input_path)
            exact_ratio = main_clip.size[0] / main_clip.size[1]
            theoretical_ratio = self.resolution[0] / self.resolution[1]

            if theoretical_ratio * 0.95 < exact_ratio < theoretical_ratio * 1.05:
                logging.debug(f"Clip aspect ratio is close to the theoretical ratio. Copying the clip.\n"
                              f"Exact: {exact_ratio}, Theoretical: {theoretical_ratio}")
                shutil.copy(input_path, output_path)
                return True

            bg = VideoFileClip(input_path).resize(self.resolution).fx(vfx.colorx, 0.1)  # Darken background
            if config.video.get('blur', False):
                bg = bg.fl_image(self.blur)
                logging.debug("Applied Gaussian blur to the background.")

            main_clip = main_clip.resize(width=self.resolution[0]).set_start(0)
            video = CompositeVideoClip([bg, main_clip.set_position("center", "center")])
            video.write_videofile(output_path, audio_codec='aac')

            logging.info(f"Rendered video saved to {output_path}")
            return True
        except PermissionError as e:
            logging.error(f"Permission error: {e}")
            return False
        except Exception as e:
            logging.error(f"An error occurred during rendering: {e}")
            return False


if __name__ == '__main__':
    # Example usage:
    directory = "path/to/your/directory"
    clip_name = "input_clip.mp4"
    output_name = "output_clip.mp4"
    resolution = (1920, 1080)

    renderer = Render(directory, clip_name, output_name, resolution)
    success = renderer.render
    if success:
        logging.info("Rendering completed successfully.")
    else:
        logging.error("Rendering failed.")
