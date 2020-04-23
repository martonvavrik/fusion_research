import flap

def convert_dict_to_flap(input_dict, skip_keys=[], create_channel_no=False):
    # input_dict: a NTI wavelet tools sav file loaded as a python dictionary,
    # preferably loaded with the io.readsav command
    # skip_keys: which keys to skip when creating coordinate axes in addition to:
    # "data", "expname", "shotnumber", "data_history", "coord_history",
    # and returns a flap.DataObject
    if type(input_dict) is not dict:
        raise TypeError('loaded_sav is not a dictionary')

    coordinates = []
    skip_keys.extend(["data", "expname", "shotnumber", "data_history", "coord_history"])

    # planned? feature: non-equidistant time axis
    if "timeax" in input_dict:
        time_ax = flap.Coordinate(name="Time",
                                  unit="s",
                                  mode=flap.CoordinateMode(equidistant=True),
                                  start=input_dict["timeax"][0],
                                  step=input_dict["timeax"][1] - input_dict["timeax"][0],
                                  # values=loaded_sav["timeax"]
                                  dimension_list=[1]
                                  )
        coordinates.append(time_ax)
        skip_keys.append("timeax")

    if "channels" in input_dict:
        channel_name = flap.Coordinate(name="Channels",
                                       unit=None,
                                       mode=flap.CoordinateMode(equidistant=False),
                                       values=input_dict["channels"],
                                       dimension_list=[0],
                                       shape=len(input_dict["channels"])
                                       )
        coordinates.append(channel_name)
        skip_keys.append("channels")

        if create_channel_no:
            channel_no = flap.Coordinate(name="Channel_no",
                                         unit="no",
                                         mode=flap.CoordinateMode(equidistant=True),
                                         start=0,
                                         step=1,
                                         dimension_list=[0]
                                         )
            coordinates.append(channel_no)

    if "theta" in input_dict:
        theta_ax = flap.Coordinate(name="Theta",
                                   unit="rad",
                                   mode=flap.CoordinateMode(equidistant=False),
                                   values=input_dict["theta"],
                                   dimension_list=[0],
                                   shape=len(input_dict["theta"])
                                   )
        coordinates.append(theta_ax)
        skip_keys.append("theta")

    if "phi" in input_dict:
        phi_ax = flap.Coordinate(name="Phi",
                                 unit="rad",
                                 mode=flap.CoordinateMode(equidistant=False),
                                 values=input_dict["phi"],
                                 dimension_list=[0],
                                 shape=len(input_dict["phi"])
                                 )
        coordinates.append(phi_ax)
        skip_keys.append("phi")

    # create coordinate objects for other keys in the dicionary
    for key in input_dict:
        if key not in skip_keys:
            try:
                unknown_ax = flap.Coordinate(name=key,
                                             unit=None,
                                             mode=flap.CoordinateMode(equidistant=False),
                                             values=input_dict[key],
                                             dimension_list=[0],
                                             shape=len(input_dict[key])
                                             )
                
                coordinates.append(unknown_ax)
                skip_keys.append(key)
            except:
                print(
                    "Could not generate flap coordinate for " + key + 
                    ". You may want to use the skip_keys argument for this key.")

    flap_object = flap.DataObject(
        data_array=input_dict['data'],
        data_unit=flap.Unit(name='voltage', unit='volt'),
        exp_id=str(input_dict['expname'])[2:-1] + " " + str(input_dict['shotnumber']),
        coordinates=coordinates,
        data_shape=input_dict['data'].shape
    )

    return flap_object
