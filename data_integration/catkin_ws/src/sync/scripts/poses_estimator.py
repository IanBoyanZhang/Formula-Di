import PyKDL as kd

# TODO: put this under meta_data?
# Global
velo_to_front = [-1.0922, 0, -0.0508]

def dict_to_vect(di):
    return kd.Vector(di["tx"], di["ty"], di["tz"])

def list_to_vect(li):
    return kd.Vector(li[0], li[1], li[2])

def frame_to_dict(frame):
    r, p, y = frame.M.GetRPY()
    return dict(tx=frame.p[0], ty=frame.p[1], tz=frame.p[2], rx=r, ry=p, rz=y)

def get_yaw(p1, p2):
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0])

def get_obstacle_pos(
	front,
	rear,
	obstacle,
	velodyne_to_front
    ):
    """
    In NED coordinate?
    This function is based on
    get_obstacle_pos in bag_to_kitti.py
	
    Here we don't calculate gps device to centroid correction
    User of this function should provide obstacle pos(e) centroid postion against 
    capture vehicle gps coordinates
	
    Elevation/pitch is not evaluated? 
    """
    front_v = dict_to_vect(front)
    rear_v = dict_to_vect(rear)
    obs_v = dict_to_vect(obstacle)

    yaw = get_yaw(front_v, rear_v) 
    rot_z = kd.Rotation.RotZ(-yaw)

    diff = obs_v - front_v
    res = rot_z * diff
    res += list_to_vec(velodyne_to_front)

    # The gps to_centroid offset of the obstacle should be rotated by 
    # the obstacle's yaw. Unfortunately
    return frame_to_dict(kd.Frame(kd.Rotation(), res))


def generate_estimate_obstacle_poses(
	cap_front_rtk,
	cap_rear_rtk,
	obs_centroid
    ):
    """
    Generator version for offline training?
    Different from generating ground truth
    Parameters:
    Pandas DF.to_dict:  dict like {column -> {index -> value}}
    http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.to_dict.html
    ----------------------
    cap_front_rtk: dict converted from Pandas DF or list?
    cap_rear_rtk: dict converted from 
    obs_centroid: dict converted from Panda DFs? During offline training, this should be generated 
    """	
    # all coordinates records should be interpolated to same sample base at this point
    assert len(cap_front_rtk) == len(cap_rear_rtk) == len(obs_centroid)
    rtk_coords = zip(cap_front_rtk, cap_rear_rtk, obs_centroid)
    output_poses = [get_obstacle_pos(c[0], c[1], c[2], velo_to_front) for c in rtk_coords]
    return output_poses

def estimate_obstacle_pose(
	cap_front_rtk_single,
    	cap_rear_rtk_single,
    	obs_centroid_single
    ):
    """
    Single frame version for online prediction?	
    Expect to be a vector?
    """
    output_poses = [get_obstacle_pos(cap_front_rtk, cap_rear_rtk, obs_centroid)]	
    return output_poses


class Motion():
    def __init__(self):
	return None

if __name__ == '__main__':
    motion_estimator = Motion()
