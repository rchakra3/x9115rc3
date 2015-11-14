# Paper Summary
## i. Yepang Liu, Chang Xu  and Shing-Chi Cheung. 2014. Characterizing and Detecting Performance Bugs for Smartphone Applications. In Proceedings of the 36th International Conference on Software Engineering

## ii. Keywords


1. **Performance Bug:** A performance bug is a problem with an application that is not a defect in its expected outputs, but instead something that affects the user experience when using the application. This is particularly important when it comes to mobile app developers since users now have multiple apps to choose from for the same functionality.

2. **Static Analysis:** Debugging an application by analyzing its code base and not executing it. Static analysis is possible when you have some set of guidelines that you expect code to follow. For example, a pep8 lint tool performs static analysis on python code to identify parts of code that do not adhere to the pep8 specification.

3. **Memory Bloat:** This refers to an application using increasingly large amounts of device memory, ultimately leading to Out of Memory type errors or the app itself crashing. Such bugs affect not only the user's experience with that particular app, but the user
s overall device experience since memory is a shared resource.

4. **Energy Leak:** The authors define energy leak as any processing/rendering that is performed in the app that has no functional use. For example rendering a UI element that remains invisible or hidden throughout the execution of the app. Such bugs lead to a mobile device's battery getting drained at a fast rate, and thus an overall bad user experience.


## iii. Artifacts

1. **Motivation:** Despite the pervasiveness of mobile applications, there are very few extensive studies on the performance bugs present in them. There have been extensive studies on performance bugs in PCs and server-side applications with proposed improvements, but it is unclear whether the same approaches would improve performance in mobile apps as well. The authors' motivation in conducting this study was to sample a large number of popular apps, identify common bugs present in them and figure out their impact on user experience.

2. **Sampling procedures:** In order to judge the pervasiveness of performance bugs in apps before conducting their study, the authors used a random sampling of 60,000 android apps from the play store. In order to select the apps for the actual study, the authors used certain criteria to narrow down the number of apps and then randomly selected 29 of them. Following this, they chose 8 of the 29 which specifically tracked performance bugs as a category of bugs. The criteria used to narrow down the apps was:
    - Popularity - More than 10,000 downloads
    - Traceability - Public bug tracking
    - Maintainability - Code revisions in the Hundreds

3. **Related Work:**
    
    1. Hao, S., Li, D., Halfond, W.G.J., and Govindan, R. 2013. Estimating mobile application energy consumption using program analysis. In Proc. 35th Int’l Conf. Sof . Engr. ICSE '13. 92-101

    2.  Kwon, Y., Lee, S., Yi, H., Kwon, D., Yang, S., Chun, B., Huang, L., Maniatis, P , Naik, M., and Paek, Y. 2013. Mantis: automatic performance prediction for smartphone applications. In Proc. USENIX Annual Tech. Conf. USENIX '13. 297-308.

    3. Nistor, A., Song, L., Marinov, D., and Lu, S. Toddler: detecting performance problems via memory-access patterns. 2013. In Proc. Int’l Conf. Soft. Engr. ICSE '13. 562-571.

    4. Jin, G., Song, L., Shi, X., Scherpelz, J., and Lu S. 2012. Understanding and detecting real-world performance bugs. In Proc. ACM SIGPLAN Conf. Programming Language Design and Implementation. PLDI '12. 77-88

4. **Baseline Results:**

    - Most Performance bugs in mobile apps are (unsurprisingly) GUI related. Since the smoothness of a touchscreen mobile application is usually a measure of user satisfaction with it, a large percentage of performance bugs are related to the UI. The core functionality of popular apps is usually to replicate functionality users have previously experienced on a desktop and thus, living up to a user's expectations can be difficult. For example, a mobile user expects their mobile browsing experience to be as smooth as their desktop browsing experience.

    - The second most common bug is Energy leak. This can indirectly be related to the UI. For example, generating UI elements in the background or generating UI elements that end up being invisible consumes battery and CPU resources without doing anything useful or adding to the user experience.

    - Memory Bloat is another common performance bug. This is usually due to an extension of my previous point about replicating the desktop experience on a much less powerful device. 
    

## iv. Future Work

1. A similar study on iOS apps would be interesting as well. Generally iOS apps tend to go through a lot more scrunity before release along with more stringent criteria for release on the iOS app store. It would be interesting to see a comparison of the two.
2. A guide based on this study which developers could refer to before starting development. Based on developer comments it seems like some bugs are due to the way the app itself was built in the beginning, with developers not having the time to completely refactor legacy code.