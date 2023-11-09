
# @bp.route("/events", methods=["POST"])
# @login_required
# @type_required("asso", "teacher", "admin")
# def add_event_route():
#     data = request.get_json()
#     # TODO: Check required fields in data
#     event_id = add_event(
#         name=data.get("name"),
#         date=data.get("date"),
#         start_time=data.get("start_time"),
#         end_time=data.get("end_time"),
#         location=data.get("location"),
#         description=data.get("description")
#     )
    
#     if event_id > 0:
#         return jsonify(message="Event added successfully", event_id=event_id, status="success"), 201
#     else:
#         return jsonify(message="Error adding event", status="error"), 500

# @bp.route("/assos/<int:asso_id>/subscribe", methods=["POST"])
# @login_required
# def subscribe_to_asso_route(asso_id):
#     success = subscribe_to_asso(current_user.user_id, asso_id)
    
#     if success:
#         return jsonify(message="Subscribed successfully", status="success"), 200
#     else:
#         return jsonify(message="Error subscribing to association", status="error"), 500

# @bp.route("/assos/<int:asso_id>/unsubscribe", methods=["DELETE"])
# @login_required
# def unsubscribe_from_asso_route(asso_id):
#     success = unsubscribe_from_asso(current_user.user_id, asso_id)
    
#     if success:
#         return jsonify(message="Unsubscribed successfully", status="success"), 200
#     else:
#         return jsonify(message="Error unsubscribing from association", status="error"), 500
    
# @bp.route("/assos", methods=["GET"])
# @login_required
# def get_all_assos_route():
#     assos = get_all_assos()
#     formatted_assos = [
#         {
#             "id": asso.user_id,
#             "name": asso.name,
#             "logo": asso.profile_pic,
#             "linkedin": asso.linkedin,
#             "subscribed": current_user in asso.subscribers  # Check if the user is a subscriber
#         }
#         for asso in assos
#     ]
#     return jsonify(formatted_assos), 200

