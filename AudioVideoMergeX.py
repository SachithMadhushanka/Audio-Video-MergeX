from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QMessageBox, QComboBox
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import os
import sys

class AudioVideoMergeX(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Video MergeX')

        self.btnCombine = QPushButton('Combine Audio with Videos', self)
        self.btnCombine.clicked.connect(self.combine_audio_with_videos)
        self.btnCombine.move(50, 50)

        self.volumeLabel = QLabel('Select Volume Scale:', self)
        self.volumeLabel.move(50, 80)

        self.volumeComboBox = QComboBox(self)
        self.volumeComboBox.addItem("10%")
        self.volumeComboBox.addItem("20%")
        self.volumeComboBox.addItem("30%")
        self.volumeComboBox.addItem("40%")
        self.volumeComboBox.addItem("50%")
        self.volumeComboBox.addItem("60%")
        self.volumeComboBox.addItem("70%")
        self.volumeComboBox.addItem("80%")
        self.volumeComboBox.addItem("90%")
        self.volumeComboBox.move(180, 80)

        self.statusLabel = QLabel(self)
        self.statusLabel.setGeometry(50, 120, 400, 20)

        self.setGeometry(300, 300, 400, 170)
        self.show()

    def combine_audio_with_videos(self):
        video_file_paths, _ = QFileDialog.getOpenFileNames(self, 'Select video files', '', 'MP4 files (*.mp4);;All files (*.*)')
        audio_file_path, _ = QFileDialog.getOpenFileName(self, 'Select audio file', '', 'MP3 files (*.mp3);;All files (*.*)')

        if video_file_paths and audio_file_path:
            audio_clip = AudioFileClip(audio_file_path)
            audio_duration = audio_clip.duration

            for video_file_path in video_file_paths:
                video_clip = VideoFileClip(video_file_path)
                video_duration = video_clip.duration

                # Repeat audio if necessary to match video duration
                if video_duration > audio_duration:
                    repetitions = int(video_duration / audio_duration) + 1
                    repeated_audio_clips = [audio_clip] * repetitions
                    audio_clip = concatenate_audioclips(repeated_audio_clips)
                    audio_clip = audio_clip.subclip(0, video_duration)

                # Adjust audio volume
                volume_percentage = int(self.volumeComboBox.currentText().replace('%', '')) / 100
                audio_clip = audio_clip.volumex(volume_percentage)

                output_dir = os.path.dirname(video_file_path)
                video_name = os.path.splitext(os.path.basename(video_file_path))[0]
                output_file_path = os.path.join(output_dir, f"{video_name}_with_audio_{self.volumeComboBox.currentText()}.mp4")

                merged_clip = video_clip.set_audio(audio_clip)
                merged_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

                # Remove previous video file
                os.remove(video_file_path)

                # Rename output video file
                os.rename(output_file_path, os.path.join(output_dir, f"{video_name}.mp4"))

            self.statusLabel.setText("Audio combined with videos and saved successfully!")
        else:
            QMessageBox.warning(self, 'Warning', 'Please select video and audio files.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioVideoMergeX()
    sys.exit(app.exec_())
