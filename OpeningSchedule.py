# Copyright 2020 Cadwork.
# All rights reserved.
# This file is part of OpeningSchedule,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

# import required controllers
import attribute_controller, element_controller, geometry_controller, list_controller, menu_controller, shop_drawing_controller, utility_controller

# get active elements
active_elements = element_controller.get_active_identifiable_element_ids()

# create opening list for filtering
active_openings = []

# filter openings
for element in active_elements:
  if attribute_controller.is_opening(element):
    active_openings.append(element)

# show standard container selection menu
standard_containers = element_controller.get_standard_container_list()
selected_container_name = menu_controller.display_simple_menu(standard_containers)

# disable check and query prompts
utility_controller.push_check_and_query_data()
utility_controller.change_check_and_query_data_to_no_queries()

# create container list to hold created containers
created_containers = []

# loop over openings
for opening in active_openings:
  # add standard container over opening
  single_opening_list = [opening]
  opening_name = attribute_controller.get_name(opening)
  container_content = element_controller.get_variant_sibling_element_ids(opening)
  container = element_controller.create_auto_container_from_standard_with_reference(single_opening_list, opening_name, selected_container_name, opening)
  created_containers.append(container)

  filtered_content = []

  for item in container_content:
    if opening == item:
      pass
    else:
      filtered_content.append(item)

  # set container content
  element_controller.set_container_contents(container, filtered_content)

  # trim container
  ref_length = geometry_controller.get_length(container)
  ref_width = geometry_controller.get_width(container)
  ref_height = geometry_controller.get_height(container)

  ref_length = ref_length - 20
  ref_width = ref_width - 20
  ref_height = ref_height - 20

  single_container_list = [container]

  geometry_controller.set_length_real(single_container_list, ref_length)
  geometry_controller.set_width_real(single_container_list, ref_width)
  geometry_controller.set_height_real(single_container_list, ref_height)

  # transfer attributes
  ref_group = attribute_controller.get_group(opening)
  ref_subgroup = attribute_controller.get_subgroup(opening)
  ref_comment = attribute_controller.get_production_number(opening)
  ref_sku = attribute_controller.get_sku(opening)
  ref_user_1 = attribute_controller.get_user_attribute(opening, 1)
  ref_user_2 = attribute_controller.get_user_attribute(opening, 2)
  ref_user_3 = attribute_controller.get_user_attribute(opening, 3)
  ref_user_4 = attribute_controller.get_user_attribute(opening, 4)
  ref_user_5 = attribute_controller.get_user_attribute(opening, 5)
  ref_user_6 = attribute_controller.get_user_attribute(opening, 6)
  ref_user_7 = attribute_controller.get_user_attribute(opening, 7)
  ref_user_8 = attribute_controller.get_user_attribute(opening, 8)
  ref_user_9 = attribute_controller.get_user_attribute(opening, 9)
  ref_user_10 = attribute_controller.get_user_attribute(opening, 10)

  attribute_controller.set_group(single_container_list, ref_group)
  attribute_controller.set_subgroup(single_container_list, ref_subgroup)
  attribute_controller.set_comment(single_container_list, str(ref_comment))
  attribute_controller.set_sku(single_container_list, ref_sku)
  attribute_controller.set_user_attribute(single_container_list, 1, ref_user_1)
  attribute_controller.set_user_attribute(single_container_list, 2, ref_user_2)
  attribute_controller.set_user_attribute(single_container_list, 3, ref_user_3)
  attribute_controller.set_user_attribute(single_container_list, 4, ref_user_4)
  attribute_controller.set_user_attribute(single_container_list, 5, ref_user_5)
  attribute_controller.set_user_attribute(single_container_list, 6, ref_user_6)
  attribute_controller.set_user_attribute(single_container_list, 7, ref_user_7)
  attribute_controller.set_user_attribute(single_container_list, 8, ref_user_8)
  attribute_controller.set_user_attribute(single_container_list, 9, ref_user_9)
  attribute_controller.set_user_attribute(single_container_list, 10, ref_user_10)

  attribute_controller.set_production_number(single_container_list, ref_comment + 10000)

filtered_containers = []
filtered_production_numbers = []

for container in created_containers:
  production_number = attribute_controller.get_production_number(container)
  if production_number not in filtered_production_numbers:
    filtered_production_numbers.append(production_number)
    filtered_containers.append(container)

# export container shop drawings
shop_drawing_controller.export_container_with_clipboard(1, filtered_containers)

# remove containers
element_controller.delete_elements(created_containers)

# restores check and query prompts
utility_controller.pop_check_and_query_data()

# display clipboard message to user
utility_controller.print_error('Clipboard 1 Ready...')
