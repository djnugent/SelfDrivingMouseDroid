# How to setup Ubuntu on a USB Stick

## Need to Test This!!!

## You'll need:
  - 2 USB sticks. One ~2gb and the other 32gb+
  - Windows PC with admin access
  - Access to your BIOS

## Step One: Create a bootable disc
  - Back up your USB sticks. They will be completely wiped.
  - Download this ISO file(Ubuntu 14.04 x64)
  - Download rufus disk imager
  - Open up rufus and select your 2gb flash drive and ubuntu ISO file you just downloaded. The default settings are fine
  - Run it

## Step Two: Boot into Ubuntu Installer
  - **Completely** power down your machine. This is best achieved by holding down the power button until it force shuts off.
  - Power up the machine with your 2gb flash drive plugged in
  - Be repeatably hitting your startup interrupt button to get into your BIOS. This is usually is f12, Enter, f2, or f10. Your startup screen should tell you but by the time you see it it might be too late. It may take multiple power attempts to get it right.
  - Once you get it right you will be kicked into your BIOS. Every BIOS is different but you are looking to for something along lines of `Boot off alternative disk`, or `Boot from USB`, or `Boot from external disk`, or `Boot manager`, etc.
  - Select your USB stick
  - This should bring you to ubuntu. When prompted you will want to select `Install Ubuntu`

## Step Three: Install Ubuntu
  - Plug in your other USB stick now
  - Follow the setup guide. No need to connect to wifi, install updates, or use 3rd party software. ***Careful***: Once it prompts you on *install location* you should select `something else`
  - This will bring you to a partition table. This will list your connected storage devices and their partitions. You should see your harddrive(s), 2 gb USB stick, and 32+ gb USB stick. We will be modifying the partition table on your 32+ gb USB so be very certain you know which one it is. Just look at the how much memory each device has and match it up with your 32+ gb USB. Probably `/dev/sdb` or `/dev/sdc`. Very unlikely it is `/dev/sda`! That's probably your harddrive! Anything ending with a number is partition, not a memory device.
  - Once you have located your device, lets call it `/dev/sdx`, we will need to clear all existing partitions **on THIS device**. As stated earlier partitions are denoted with numbers i.e. `/dev/sdx1`, `/dev/sdx2`, `/dev/sdx#`...
  - Select a partition. Then look to the lower left of main box and you will see a couple buttons. Select the one that allows you to wipe/format/delete the partition. Do this for all partitions on the device. Click continue/agree when prompted by all the warnings.
  - Now we should have just one partition that says `Free space`. We are going to create 2 new partitions. Select the free space and click to `+` button in the left lower corner. Call the partition "swap" and give it 2048mb of space, and it's type should be "Linux Swap"
  - Now you should have 2 partitions, `Free Space` and `Swap`. We are going to add another partition to `Free space` called "Main" By default it will take up the rest of space so you don't have to change it's space. The type should be "Ext4 Linux". You should mount it `/`
  - Now you should have 2 partitions and no free space.
  - **Important**: In the drop down menu at bottom of the screen bes sure you have your 32+ drive selected `/dev/sdx`
  - Now click install!
  - Follow the rest of the prompts until you are complete

## Step Four: Run Ubuntu
  - You can unplug your 2gb flash drive and keep your 32+ gb flash drive plugged in.
  - Completely power down your computer like before. And follow the same procedure to boot off a USB stick. This will bring you to a menu where you will select Ubuntu.
  - Congrats you are now running ok-ist operating system around

## Step Five(Optional): Setup your environment
  - Connect to wifi
  - Open terminal and run `sudo apt-get update`
  - Run `sudo apt-get upgrade`
  - Install docker engine and nvidia-docker engine

## TODO:
  - Figure out how to install Nvidia driver without clobbering your system
  - `sudo apt-get install nvidia-375 nvidia-settings nvidia-common`
  - `sudo update-alternatives --config x86_64-linux-gnu_gl_conf` select 0
  - `sudo nvidia-xconfig`
  - `sudo ldconfig`
  - Reboot
