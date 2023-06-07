-- this file was manually created
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown', 'cupola.potted-0k@icloud.com', '4f4baece-5966-4691-8ecd-f6d41f00b981'),
  ('Andrew Bayko', 'bayko', 'sawbuck_bail_0m@icloud.com', 'b99a2447-162e-4dc7-a88c-bd8c669dbef4');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
