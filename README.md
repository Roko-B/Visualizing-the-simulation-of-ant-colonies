# Modeling-simple-ant-colonies-using-differential-equations
Modeling the growth of simple two variable colonies of ants.<br/>
This model is based on two differential equations shown bellow:<br/>
$\frac{dF}{dt}=-aC$<br/>
$\frac{dC}{dt}=bF$<br/>
where $F$ is the amount of food, $C$ is the size of the colony and the coefficients $a$ and $b$ are traits of the colony and food.<br/>
If the amount of food is negative it means that there isnt enough food to supply the colony.<br/>
If the size of the colony is negative that means that the colony is small enough for the food to be able to replenish itself.<br/>
<br/>
The actual simulation isnt carried out by the analytical soution to this set of ODEs as I do not know how to find the solution to them. Rather it is an approximation gotten by setting $dt$ to a very small value so that the resulting set of data is as close to the actual solution as possible.<br/>
This approach to solving the ODEs is a common one for equations that have no analytical answer, such as: $\ddot{\theta}(t)=-\mu\dot{\theta}(t)-\frac{g}{L}\sin{\theta(t)}$
