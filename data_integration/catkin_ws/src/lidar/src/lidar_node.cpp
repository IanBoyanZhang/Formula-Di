// ROS Point Cloud DEM Generation
#include <cmath>
#include <vector>
#include <float.h>
#include <stdio.h>
#include <math.h> 
#include <sstream>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>

#include <cv_bridge/cv_bridge.h>
#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <ros/ros.h>
#include <ros/console.h>
#include <sensor_msgs/PointCloud2.h>

#define IMAGE_HEIGHT	701
#define IMAGE_WIDTH	801
#define BIN		0.1

using namespace cv;

// Global Publishers/Subscribers
ros::Subscriber subPointCloud;
ros::Publisher pubPointCloud;

pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_grid (new pcl::PointCloud<pcl::PointXYZ>);

void iterate_through_pc(pcl::PointCloud<pcl::PointXYZ>& cloud){

}

void coordinate_transform(){

}

// main generation function
void lidar_reader(const sensor_msgs::PointCloud2ConstPtr& pointCloudMsg)
{
  ROS_DEBUG("Point Cloud Received");

  // Convert from ROS message to PCL point cloud
  pcl::fromROSMsg(*pointCloudMsg, *cloud);
  size_t num_points = cloud->points.size();
  ROS_INFO("Num:%zu", num_points);
  for (size_t iter=0; iter<num_points; iter+=1) {
    ROS_INFO("x->:%f", cloud->points[iter].x);
    ROS_INFO("y->:%f", cloud->points[iter].y);
    ROS_INFO("z->:%f", cloud->points[iter].z);
  }
}

int main(int argc, char** argv)
{
  ROS_INFO("Starting LIDAR Node");
  ros::init(argc, argv, "lidar_node");
  ros::NodeHandle nh;

  subPointCloud = nh.subscribe<sensor_msgs::PointCloud2>("/velodyne_points", 2, lidar_reader);
//  pubPointCloud = nh.advertise<sensor_msgs::PointCloud2> ("/heightmap/pointcloud", 1);

  ros::spin();

  return 0;
}
