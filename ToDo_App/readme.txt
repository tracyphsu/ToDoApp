5/19/21- Ashley
------------------------------------------------
make sure virtual env is active
cd into the project folder
install this in terminal: pip install google-api-python-client

superuser created
username: admin
password: adminpassword

username: johndoe
password: adminpassword

username: sallysue
password: adminpassword


5/20/21- Ashley 
-------------------------------------------------
Forgot to create branch but I hadn't done anything yet besides delete what I thought was an extra folder in the templates folder (which i ended up putting back LOL) Went ahead and pushed it to master. Then created a branch  named ashley

updated task_list.html
created DetailView, CreateView, DeleteView, UpdateView, FormView
created more templates
created/completed login/registration with templates

*I noticed he had in the Task model "complete" and you put "status"- I do think status is better but that will need to be changed eventually to a charfield as a booleanfield would not make sense but we can update that when its necessary. I'll leave it for now. 

created another user in the admin panel so you could see different accounts to compare- login info listed above below the superuser login info; created another user sallysue to test registration- info up above as well

Left Off at 1:32:10 in the youtube video- at this point the login/registration is up and running, as well as view task detail, edit and delete functions. 

5/21/21- Ashley
I added the grocery list templates- basically made it the same as the tasks list. Ideally, I think the complete "button" should be on the front side and not have to go into the "update"form just to check it. And also ideally, I'd like to add items to the list without having to redirect to the page where you add an item. That would be time consuming. So I'll try to figure out how we can do that. 

I updated some CSS...I thought it might be nice to stick with that gradient feature and just let each tab be a different color. 

I think I might have messed up the container or something somehow...The colored box at the top is not the full width of the app but we can figure that out later as well.

I'm not entirely sure how we should do the meal planner tab...I was just wanting it to be pretty simple...Where it's a list of the week days, like this: 
Sunday: Write a meal here
Monday: Spaghetti w/ Salad
Tuesday: Steak and Broccoli
Wednesday: etc..
Thursday:
Friday:
Saturday:

It's like a hidden text box where they can write in what they want to eat for that day. I didn't want to make it complicated where they have to choose from a recipe box or anything like that- although that is maybe something that could come later. I purposefully wanted this to specifically be something to just input what you're planning on making. What do you think? or if you have a better idea..i'm all ears.

Lastly, my nav bar is supposed to only highlight the tab that's clicked. Only the Tasks and the Grocery list tabs are workable right now. but you should see that when you click on Grocery list- the tasks tab stays highlighted. I had it working at one point and I'm not sure what I did wrong so I'll have to figure it out. If you have time and want to- you can go to bootstrap website and find their nav and tabs components to read about it and see what I did= that's where I got the code from. 

Sorry my notes are so long! Let me know if you need anything else. 


5/21/21 - Tracy
Love your notes!

<<<<<<< HEAD
5/21/21 - Tracy
Love your notes!

ok yay I made it so you can click on the icons to mark them complete/incomplete!

Yes! I was thinking the exact same with the different color gradiants based on the new tabs. Yay!

I'm not sure if you even broke anything with the header margin - I couldn't find anything but I did a work around to make it full width... hahaha 

Meal Planner:
Ok I have a few thoughts on this so I wanted to touch base with you before we did anything. I agree with your format, but I'm wondering how we can set the days. I was thinking it would be cool if it's one form and they can select the days of the week and we can figure out the function to display per day of the week and the meals in them. However, I can't think of a way to set it so it's in the right order (Sunday, Monday, Tuesday, etc). Or we can just manually type out the days of the week and then have separate forms under it? I didn't try any of them so maybe there's something out there that works. I did do a quick google and youtube search and only found this one: https://www.programmersought.com/article/45865696412/ but no idea what it looks like. I figured I will work on the other stuff first and we can decide on that together. 
But yes, I also want to keep it as simple as we can.

I fixed the tab highlighting issue (I think you just copied and pasted so the wrong tab was "active"). Thanks for finding that code tho, it's super cool!! I also centered the nav bar as much as I could. 

Ok so I started watching this video:
https://www.youtube.com/watch?v=j1mh0or2CX8
https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322

I'm not sure how I feel about it hahaha ... I'm only like 8 min in, but I guess he's doing everything in terminal so probably going to take some time to figure out how to put it all in models/views. 
Maybe there is a better video out there!

I think we're almost there!! Just need to figure out how we should format the meal planner but once we do it should be easy and then the calendar!
And then... are we done? :):)!


=======
ok yay I made it so you can click on the icons to mark them complete/incomplete!
>>>>>>> d16c1c3826809ff18b9024eeeec64b0de8ca51d3

Yes! I was thinking the exact same with the different color gradiants based on the new tabs. Yay!

I'm not sure if you even broke anything with the header margin - I couldn't find anything but I did a work around to make it full width... hahaha 

Meal Planner:
Ok I have a few thoughts on this so I wanted to touch base with you before we did anything. I agree with your format, but I'm wondering how we can set the days. I was thinking it would be cool if it's one form and they can select the days of the week and we can figure out the function to display per day of the week and the meals in them. However, I can't think of a way to set it so it's in the right order (Sunday, Monday, Tuesday, etc). Or we can just manually type out the days of the week and then have separate forms under it? I didn't try any of them so maybe there's something out there that works. I did do a quick google and youtube search and only found this one: https://www.programmersought.com/article/45865696412/ but no idea what it looks like. I figured I will work on the other stuff first and we can decide on that together. 
But yes, I also want to keep it as simple as we can.

I fixed the tab highlighting issue (I think you just copied and pasted so the wrong tab was "active"). Thanks for finding that code tho, it's super cool!! I also centered the nav bar as much as I could. 

Ok so I started watching this video:
https://www.youtube.com/watch?v=j1mh0or2CX8
https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322

I'm not sure how I feel about it hahaha ... I'm only like 8 min in, but I guess he's doing everything in terminal so probably going to take some time to figure out how to put it all in models/views. 
Maybe there is a better video out there!

I think we're almost there!! Just need to figure out how we should format the meal planner but once we do it should be easy and then the calendar!
And then... are we done? :):)!

Also - redeployed, but I can only do it off the Master! I'll do it again tomorrow. I need the practice hahaha. Also, do you have an iphone? I can share my notes for deployment. Well I just copied and pasted it off the website but easier to follow I think. 
